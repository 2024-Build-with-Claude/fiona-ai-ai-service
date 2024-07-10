import logging
import os
import shelve
import time
from email import message

from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session

from app.models.message_model import Message
from app.models.message_thread_model import MessageThread


def create_thread(
    db_session: Session,
    mufasa_ai_resume_id: str | None = None,
    whatsapp_id: str | None = None,
    open_ai_thread_id: str | None = None,
    line_id: str | None = None,
    platform: str = "whatsapp",
):
    """
    Create a new thread
    """
    logging.info(f"start create_thread: {mufasa_ai_resume_id}")
    message_thread = MessageThread(
        whatsapp_id=whatsapp_id,
        line_id=line_id,
        mufasa_ai_resume_id=mufasa_ai_resume_id,
        open_ai_thread_id=open_ai_thread_id,
        platform=platform,
    )
    db_session.add(message_thread)
    db_session.commit()
    db_session.refresh(message_thread)
    logging.info(f"end create_thread: {message_thread}")
    return message_thread


def get_thread_by_mufasa_ai_resume_id(
    mufasa_ai_resume_id: str, db_session: Session
) -> MessageThread | None:
    """
    Get a thread by mufasa_ai_resume_id
    """
    logging.info(f"start get_thread_by_mufasa_ai_resume_id: {mufasa_ai_resume_id}")
    thread = (
        db_session.query(MessageThread)
        .filter(MessageThread.mufasa_ai_resume_id == mufasa_ai_resume_id)
        .first()
    )
    logging.info(f"end get_thread_by_mufasa_ai_resume_id: {thread}")
    return thread
