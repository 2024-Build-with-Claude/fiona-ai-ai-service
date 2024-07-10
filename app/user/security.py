from jose import jwt
from passlib.context import CryptContext
from firebase_admin import auth as firebase_auth
from fastapi import HTTPException, status

from app.config.settings import settings


def hash_password(raw: str) -> str:
    """This function hashes a password

    Args:
        raw (str): The raw password

    Returns:
        str: The hashed password
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(raw)


def verify_password(plain_password: str, hashed_password: str):
    """This function verifies a password

    Args:
        plain_password (str): The plain password
        hashed_password (str): The hashed password

    Returns:
        bool: True if the password is correct, False otherwise
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """This function creates a JWT token

    Args:
        data (dict): The data to be encoded

    Returns:
        str: The JWT token
    """
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.HASHING_ALGORITHM)

def verify_firebase_token(token: str):
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )
