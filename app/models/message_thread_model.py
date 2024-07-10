import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import DBBase


class MessageThread(DBBase):
    """Message Thread model"""

    __tablename__ = "message_threads"

    id = Column(
        String, primary_key=True, unique=True, default=lambda: str(uuid.uuid4())
    )
    # wa_id = Column(String(36))
    line_id = Column(String(36), nullable=True)
    whatsapp_id = Column(String(36), nullable=True)
    fiona_ai_resume_id = Column(String(36), nullable=True)
    open_ai_thread_id = Column(String, unique=True)
    messages = relationship("Message", back_populates="thread")
    platform = Column(String(10), nullable=True, default="whatsapp")
    # platform can be: fiona_ai, line, whatsapp
