from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.user import schemas, security, services

router = APIRouter()


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
def user_create(user: schemas.UserCreate, db_session: Session = Depends(get_db)):
    """User create"""
    # Directly call the service function to create a new user
    return services.create_user(user=user, db=db_session)


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Token,
)
def user_login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    # Directly call the service function to login
    return services.login_user(user_credentials=user, db=db)


@router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=schemas.User,
)
def user_details(
    user: schemas.User = Depends(services.get_current_user_base_on_config),
):
    # Directly return the user obj
    return user


@router.put(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=schemas.User,
)
def update_current_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(services.get_current_user_base_on_config),
):
    """
    Update the currently authenticated user.
    """
    updated_user = services.update_user(
        user_id=current_user.id, user_update=user_update, db=db
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    return updated_user


# Admin only route
# @router.put(
#     path="/update/{user_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=schemas.User,
# )
# def update_user(
#     user_id: int,
#     user_update: schemas.UserUpdate,
#     db: Session = Depends(get_db),
# ):
#     """
#     Update a user.
#     """
#     # Call the service function to update the user
#     updated_user = services.update_user(user_id=user_id, user_update=user_update, db=db)
#     if not updated_user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this id does not exist in the system",
#         )
#     return updated_user
