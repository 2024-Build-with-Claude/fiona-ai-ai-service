import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.config.database import DBBase


class Message(DBBase):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    thread_id = Column(String, ForeignKey("message_threads.id"), nullable=False)
    sender = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    thread = relationship("MessageThread", back_populates="messages")
