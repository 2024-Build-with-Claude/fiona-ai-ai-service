from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.record.schemas import record_schema
from app.infrastructure.schemas import PageableParamDTO, PageableResultDTO
from fastapi import status
from datetime import datetime

from app.record.models import record_model


def create_record(
    record: record_schema.RecordCreate, user_id: str, db: Session
) -> record_schema.Record:
    """This function creates a new record entry in the database

    Args:
        record (schemas.RecordCreate): The record schema obj
        db (Session): The DB session

    Returns:
        models.Record: The created record obj
    """
    obj = record_model.Record(**record.model_dump(), user_id=user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_record(record_id: str, db: Session) -> record_schema.Record | None:
    """This function retrieves a record entry from the database by its id

    Args:
        record_id (str): The id of the record
        db (Session): The DB session

    Returns:
        models.Record: The retrieved record obj
    """
    return (
        db.query(record_model.Record)
        .filter(record_model.Record.id == record_id)
        .first()
    )


def get_records(
    page_params: PageableParamDTO,
    db: Session,
    user_id: str,
    sort_by: str = "end_time",
    query_start_time: datetime | None = None,
    query_end_time: datetime | None = None,
) -> PageableResultDTO[record_schema.Record]:
    """
    Retrieves multiple record entries from the database with optional time range filtering.

    Args:
        page_params (PageableParamDTO): The pagination parameters.
        db (Session): The database session.
        user_id (str): The user ID.
        sort_by (str, optional): The field to sort the records by. Defaults to "end_time".
        query_start_time (datetime | None, optional): The start time for filtering. Defaults to None.
        query_end_time (datetime | None, optional): The end time for filtering. Defaults to None.

    Returns:
        PageableResultDTO[schemas.Record]: The list of retrieved record objects with pagination info.
    """
    query = db.query(record_model.Record).filter(record_model.Record.user_id == user_id)

    # Apply time range filtering if parameters are provided
    if query_start_time:
        query = query.filter(record_model.Record.end_time >= query_start_time)
    if query_end_time:
        query = query.filter(record_model.Record.start_time <= query_end_time)

    total = query.count()

    records = (
        query.order_by(desc(getattr(record_model.Record, sort_by)))
        .offset(page_params.offset)
        .limit(page_params.size)
        .all()
    )

    record_schemas = [record.to_schema() for record in records]
    page = page_params.offset // page_params.size + 1
    result = PageableResultDTO(
        total=total, page=page, size=page_params.size, data=record_schemas
    )

    return result


def update_record(
    record_id: str, record_update: record_schema.RecordUpdate, db: Session
):
    """
    This function updates a record's details in the database.

    Args:
        record_id (str): The ID of the record to update.
        record_update (schemas.RecordUpdate): The new details of the record.
        db (Session): The DB session.

    Returns:
        models.Record: The updated record object.
    """
    record = (
        db.query(record_model.Record)
        .filter(record_model.Record.id == record_id)
        .first()
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    for var, value in vars(record_update).items():
        setattr(record, var, value) if value else None
    db.commit()
    db.refresh(record)
    return record


def delete_record(record_id: str, db: Session):
    """
    This function deletes a record from the database.

    Args:
        record_id (str): The ID of the record to delete.
        db (Session): The DB session.

    Returns:
        str: A message indicating the record was deleted.
    """
    record = (
        db.query(record_model.Record)
        .filter(record_model.Record.id == record_id)
        .first()
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    db.delete(record)
    db.commit()
    return "Record deleted"
