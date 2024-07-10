import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import DBBase


class CreditType(DBBase):
    """
    Credit type model
    can be used to track the credit type for a user
    only can be write in migration file
    """

    __tablename__ = "credit_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_credits = relationship("UserCredit", back_populates="credit_type")
    transactions = relationship("CreditTransaction", back_populates="credit_type")
    created_at = Column(DateTime, default=datetime.utcnow)


class UserCredit(DBBase):
    __tablename__ = "user_credits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    credit_type_id = Column(Integer, ForeignKey("credit_types.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    user = relationship("User", back_populates="credits")
    credit_type = relationship("CreditType", back_populates="user_credits")
    created_at = Column(DateTime, default=datetime.utcnow)


class CreditTransaction(DBBase):
    __tablename__ = "credit_transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    credit_type_id = Column(Integer, ForeignKey("credit_types.id"), nullable=False)
    transaction_type = Column(
        Enum("gain", "spend", name="transaction_type"), nullable=False
    )
    amount = Column(Integer, nullable=False)
    user = relationship("User", back_populates="transactions")
    credit_type = relationship("CreditType", back_populates="transactions")
    created_at = Column(DateTime, default=datetime.utcnow)
