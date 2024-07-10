from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.schemas import PageableParamDTO, PageableResultDTO
from app.record.models.point_transaction_model import PointTransaction
from sqlalchemy import or_
from app.record.schemas import (
    point_transaction_schema,
)


def create_point_transaction(
    transaction_data: point_transaction_schema.PointTransactionCreate, db: Session
) -> point_transaction_schema.PointTransaction:
    new_transaction = PointTransaction(**transaction_data.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction.to_schema()


def get_point_transaction(
    transaction_id: str, db: Session
) -> point_transaction_schema.PointTransaction:
    transaction = (
        db.query(PointTransaction).filter(PointTransaction.id == transaction_id).first()
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Point Transaction not found"
        )
    return transaction.to_schema()


def get_point_transactions(
    page_params: PageableParamDTO, db: Session, user_id: str
) -> PageableResultDTO[point_transaction_schema.PointTransaction]:
    query = db.query(PointTransaction).filter(
        or_(
            PointTransaction.from_user_id == user_id,
            PointTransaction.to_user_id == user_id,
        )
    )  # Adjust the filter as needed

    total = query.count()
    transactions = query.offset(page_params.offset).limit(page_params.size).all()

    transaction_schemas = [transaction.to_schema() for transaction in transactions]
    page = page_params.offset // page_params.size + 1
    result = PageableResultDTO(
        total=total, page=page, size=page_params.size, data=transaction_schemas
    )

    return result


def update_point_transaction(
    transaction_id: str,
    transaction_update: point_transaction_schema.PointTransactionUpdate,
    db: Session,
) -> point_transaction_schema.PointTransaction:
    transaction = (
        db.query(PointTransaction).filter(PointTransaction.id == transaction_id).first()
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Point Transaction not found"
        )

    for var, value in vars(transaction_update).items():
        setattr(transaction, var, value) if value is not None else None

    db.commit()
    db.refresh(transaction)
    return transaction.to_schema()


def delete_point_transaction(transaction_id: str, db: Session) -> str:
    transaction = (
        db.query(PointTransaction).filter(PointTransaction.id == transaction_id).first()
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Point Transaction not found"
        )

    db.delete(transaction)
    db.commit()
    return "Point Transaction deleted"
