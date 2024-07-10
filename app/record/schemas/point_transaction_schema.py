from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PointTransactionBase(BaseModel):
    amount: int = Field(..., description="The amount of points in the transaction")
    reason: Optional[str] = Field(
        None, max_length=255, description="The reason for the transaction"
    )


class PointTransactionCreate(PointTransactionBase):
    from_user_id: str = Field(..., description="The ID of the user sending points")
    to_user_id: str = Field(..., description="The ID of the user receiving points")


class PointTransactionUpdate(PointTransactionBase):
    pass


class PointTransaction(PointTransactionBase):
    id: str = Field(..., description="The unique identifier of the transaction")
    from_user_id: str = Field(..., description="The ID of the user sending points")
    to_user_id: str = Field(..., description="The ID of the user receiving points")
    created_at: datetime = Field(
        ..., description="The timestamp when the transaction was created"
    )
