import logging
from sqlalchemy.orm import Session

from app.models.message_model import Message


def create_message(
    message_thread_id: str, sender: str, content: str, db_session: Session
):
    """
    Create a message
    """
    logging.info(f"start create_message: {message_thread_id}, {sender}, {content}")
    message = Message(thread_id=message_thread_id, sender=sender, content=content)
    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)
    logging.info(f"end create_message: {message}")
    return message
