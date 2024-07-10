# type: ignore
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from app.config.database import DBBase
import uuid

from app.record.schemas import tag_schema
from app.record.models import association


class Tag(DBBase):
    """Tag model"""

    __tablename__ = "tags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    # Relationship to User model
    user = relationship("User", back_populates="tags")

    # New many-to-many relationship to Records
    records = relationship(
        "Record", secondary=association.tag_record_association, back_populates="tags"
    )

    # New many-to-many relationship to RecordTemplates
    record_templates = relationship(
        "RecordTemplate",
        secondary=association.tag_record_template_association,
        back_populates="tags",
    )

    def to_schema(self) -> tag_schema.Tag:
        """
        Convert the tag object to a schema object.
        Returns:
            TagSchema: The schema object representing the tag.
        """
        return tag_schema.Tag(
            id=self.id,
            name=self.name,
            user_id=self.user_id,
            created_at=self.created_at,
        )
