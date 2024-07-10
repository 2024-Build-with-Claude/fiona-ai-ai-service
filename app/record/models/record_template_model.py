# type: ignore
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, ARRAY
from sqlalchemy.orm import relationship
from app.config.database import DBBase
from app.record.schemas import record_schema, record_template_schema
import uuid
from app.record.models import association


class RecordTemplate(DBBase):
    """Record template model"""

    __tablename__ = "record_templates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    default_title = Column(String(100), nullable=False)
    default_focus = Column(Integer, nullable=False)
    default_point = Column(Integer, nullable=False)
    default_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    user = relationship("User", back_populates="record_templates")

    tags = relationship(
        "Tag",
        secondary=association.tag_record_template_association,
        back_populates="record_templates",
    )

    def to_schema(self) -> record_template_schema.RecordTemplate:
        """
        Convert the record template object to a schema object.
        Returns:
            RecordTemplateSchema: The schema object representing the record template.
        """
        return record_template_schema.RecordTemplate(
            id=self.id,
            user_id=self.user_id,
            default_title=self.default_title,
            default_focus=self.default_focus,
            default_point=self.default_point,
            default_note=self.default_note,
            created_at=self.created_at,
        )
