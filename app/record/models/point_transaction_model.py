from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.config.database import DBBase
import uuid

from app.record.schemas import point_transaction_schema


class PointTransaction(DBBase):
    """Point Transaction model"""

    __tablename__ = "point_transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=True)
    from_user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    to_user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    # Relationships
    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "reason": self.reason,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
            "created_at": self.created_at.isoformat(),
        }

    def to_schema(self) -> point_transaction_schema.PointTransaction:
        """
        Converts the model to a schema
        """
        return point_transaction_schema.PointTransaction(
            id=self.id,
            amount=self.amount,
            reason=self.reason,
            from_user_id=self.from_user_id,
            to_user_id=self.to_user_id,
            created_at=self.created_at,
        )
