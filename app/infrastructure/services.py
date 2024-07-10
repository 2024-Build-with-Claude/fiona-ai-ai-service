from sqlalchemy.orm import Session

from app.record.schemas import record_schema
from app.record.models import record_model


def create_record(record: record_schema.RecordCreate, db: Session):
    """This function creates a new record entry in the database

    Args:
        record (schemas.RecordCreate): The record schema obj
        db (Session): The DB session

    Returns:
        models.Record: The created record obj
    """
    obj = record.Record(**record.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
