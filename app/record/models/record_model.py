from datetime import datetime
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.config.database import DBBase
from app.record.schemas import record_schema
import uuid
from app.record.models import association


class Record(DBBase):
    """Record model"""

    __tablename__ = "records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    title = Column(String(100), nullable=False)
    note = Column(Text, nullable=True)
    focus = Column(Integer, nullable=False)
    point = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    # user
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="records")

    tags = relationship(
        "Tag", secondary=association.tag_record_association, back_populates="records"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "title": self.title,
            "note": self.note,
            "focus": self.focus,
            "point": self.point,
            "created_at": self.created_at.isoformat(),
        }

    def to_schema(self) -> record_schema.Record:
        """
        Convert the record object to a schema object.
        Returns:
            schemas.Record: The schema object representing the record.
        """
        return record_schema.Record(
            id=self.id,
            start_time=self.start_time,
            end_time=self.end_time,
            title=self.title,
            note=self.note,
            focus=self.focus,
            point=self.point,
            created_at=self.created_at,
        )
