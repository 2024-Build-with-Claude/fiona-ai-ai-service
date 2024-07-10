import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.config.database import DBBase


class User(DBBase):
    """User model"""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(
        String(250), nullable=True
    )  # Password can be nullable for Firebase users
    user_is_from_firebase_auth = Column(Boolean, default=False)
    auth_id = Column(String(250), nullable=True)
    is_active = Column(Boolean, default=True)
    # If the user account is disabled or not
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    records = relationship(
        "Record", back_populates="user", cascade="all, delete, delete-orphan"
    )
    record_templates = relationship(
        "RecordTemplate", back_populates="user", cascade="all, delete, delete-orphan"
    )
    tags = relationship(
        "Tag", back_populates="user", cascade="all, delete, delete-orphan"
    )
    talent_queries = relationship(
        "TalentQuery", back_populates="user", cascade="all, delete, delete-orphan"
    )
    credits = relationship("UserCredit", back_populates="user")
    transactions = relationship("CreditTransaction", back_populates="user")
