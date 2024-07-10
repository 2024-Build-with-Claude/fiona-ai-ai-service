from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.credit_type_enum import CreditTypeEnum
from app.enums.transaction_type_enum import TransactionTypeEnum
from app.infrastructure.logger import log_message
from app.models.credit_model import CreditTransaction, CreditType, UserCredit
from app.user.models import User


def consume_credits(
    user_id: str,
    credit_type_name: CreditTypeEnum,
    amount: int,
    db_session: Session,
):
    """
    Consume credits for a user, raise an error if the user does not have enough credits
    Make transaction for the user
    """
    user_credit = (
        db_session.query(UserCredit)
        .join(CreditType)
        .filter(UserCredit.user_id == user_id, CreditType.id == credit_type_name.value)
        .first()
    )

    if not user_credit or user_credit.amount < amount:
        log_message(
            level="error",
            event="Insufficient credits",
            user_id=user_id,
            credit_type_name=credit_type_name.value,
            amount=amount,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient credits"
        )

    user_credit.amount -= amount
    transaction = CreditTransaction(
        user_id=user_id,
        credit_type_id=user_credit.credit_type_id,
        transaction_type=TransactionTypeEnum.SPEND.value,
        amount=amount,
    )
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(user_credit)


def add_credits(
    user_id: str,
    amount: int,
    db_session: Session,
    credit_type_name: CreditTypeEnum,
):
    """Add credits to a user's account.

    Args:
        user_id (int): The ID of the user.
        amount (int): The amount of credits to add.
        db_session (Session): The database session.
    """
    user = db_session.query(User).filter(User.id == user_id).first()
    if user:
        # create user credit if not exists
        user_credit = UserCredit(
            user_id=user_id, credit_type_id=credit_type_name.value, amount=amount
        )
        db_session.add(user_credit)
        db_session.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")

    # add transaction for the user
    transaction = CreditTransaction(
        user_id=user_id,
        credit_type_id=credit_type_name.value,
        transaction_type=TransactionTypeEnum.SPEND.value,
        amount=amount,
    )

    return transaction
