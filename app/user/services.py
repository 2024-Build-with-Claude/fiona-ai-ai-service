import logging.config
from datetime import datetime

from fastapi import Depends, HTTPException, logger, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.dependencies import get_db
from app.enums.credit_type_enum import CreditTypeEnum
from app.services.credit_service import add_credits
from app.user import models, schemas, selectors
from app.user.exceptions import InvalidTokenException
from app.user.security import (
    create_access_token,
    hash_password,
    verify_firebase_token,
    verify_password,
)
from app.user.validators import validate_user

# NOTE: This doesnt allow login with email and password on the swagger docs
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="user/login")


def create_user(user: schemas.UserCreate, db: Session):
    """This function creates a new user entry in the database

    Args:
        user (schemas.UserCreate): The user schema obj
        db (Session): The DB session

    Returns:
        models.User: The created user obj
    """
    validate_user(user=user, db=db)
    obj = models.User(**user.model_dump())
    obj.password = hash_password(raw=user.password)
    db.add(obj)
    db.commit()
    db.refresh(obj)

    # add credits for the user
    add_credits(
        user_id=obj.id,
        amount=100,
        db_session=db,
        credit_type_name=CreditTypeEnum.CONTACT_CREDIT,
    )
    return obj


def login_user(user_credentials: schemas.UserLogin, db: Session):
    """This function logs in a user

    Args:
        user_credentials (schemas.UserLogin): The user login schema obj
        db (Session): The DB session

    Returns:
        schemas.Token: The JWT token
    """
    user = authenticate_user(
        email=user_credentials.email, password=user_credentials.password, db=db
    )
    access_token = create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="Bearer")


def authenticate_user(email: str, password: str, db: Session):
    """This function authenticates a user

    Args:
        email (str): The user's email
        password (str): The user's password
        db (Session): The DB session

    Raises:
        HTTPException[400]: Incorrect email or password
        HTTPException[404]: User not found

    Returns:
        models.User: The authenticated user obj
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not verify_password(plain_password=password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    user.last_login = datetime.now()
    db.commit()
    db.refresh(user)
    return user


def get_current_user_base_on_config(
    token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)
) -> models.User:
    """This function gets the current user based on the auth method

    Args:
        token (str): The JWT token
        db (Session): The DB session

    Returns:
        models.User: The authenticated user obj
    """
    if token == "test_token":
        # return test user
        user = selectors.get_user(email="liliangjya@gmail.com", db=db)
        return user
    
    if settings.AUTH_METHOD == "firebase":
        return get_current_user_firebase_auth(token=token, db_session=db)
    else:
        return get_current_user_local_auth(token=token, db=db)


def get_current_user_local_auth(
    token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)
) -> models.User:
    """This function gets the current user from the local auth

    Args:
        token (str): The JWT token
        db (Session): The DB session

    Returns:
        models.User: The authenticated user obj
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.HASHING_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise InvalidTokenException
        user = selectors.get_user(email=email, db=db)
        return user
    except JWTError:
        raise InvalidTokenException


def get_current_user_firebase_auth(
    token: str = Depends(OAUTH2_SCHEME), db_session: Session = Depends(get_db)
) -> models.User:
    """This function gets the current user from the firebase auth

    Args:
        token (str): The JWT token
        db (Session): The DB session

    Returns:
        models.User: The authenticated user obj
    """
    try:
        firebase_user = verify_firebase_token(token=token)
        email = firebase_user.get("email")
        if email is None:
            raise InvalidTokenException

        # use query to get user
        user = db_session.query(models.User).filter(models.User.email == email).first()

        # log
        logging.info(f"User {user}")

        if not user:
            # Create a new user in the local database if not exists
            user = models.User(
                id=firebase_user["uid"],
                email=email,
                username=email,
                is_active=True,
                created_at=datetime.now(),
                user_is_from_firebase_auth=True,
            )
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)

            # add initial credits
            add_credits(
                user_id=user.id,
                amount=100,
                db_session=db_session,
                credit_type_name=CreditTypeEnum.CONTACT_CREDIT,
            )
        return user
    except JWTError:
        raise InvalidTokenException


def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session):
    """
    This function updates a user's details in the database.

    Args:
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): The new details of the user.
        db (Session): The DB session.

    Returns:
        models.User: The updated user object.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    for var, value in vars(user_update).items():
        setattr(user, var, value) if value else None
    db.commit()
    db.refresh(user)
    return user


def delete_user(user_id: int, db: Session):
    """
    This function deletes a user from the database.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session): The DB session.

    Returns:
        str: A message indicating the user was deleted.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db.delete(user)
    db.commit()
    return "User deleted"
