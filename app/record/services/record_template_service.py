from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.infrastructure.schemas import PageableParamDTO, PageableResultDTO
from app.record.models import record_template_model
from app.record.schemas import record_template_schema

from app.record.schemas.record_template_schema import RecordTemplateCreate


def create_record_template(template: RecordTemplateCreate, user_id: str, db: Session):
    """
    Create a new record template.

    Args:
        template (RecordTemplateCreate): The details of the new record template.
        user_id (str): The ID of the user creating the template.
        db (Session): The DB session.

    Returns:
        RecordTemplate: The created record template.
    """
    new_template = record_template_model.RecordTemplate(
        **template.dict(), user_id=user_id
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template


def get_record_template(template_id: str, db: Session):
    """
    Get a record template by its ID.

    Args:
        template_id (str): The ID of the record template to get.
        db (Session): The DB session.

    Returns:
        RecordTemplate: The requested record template.
    """

    return (
        db.query(record_template_model.RecordTemplate)
        .filter(record_template_model.RecordTemplate.id == template_id)
        .first()
    )


def get_record_templates(
    page_params: PageableParamDTO,
    db: Session,
    user_id: str,
) -> PageableResultDTO[record_template_schema.RecordTemplate]:
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
        PageableResultDTO[schemas.RecordTemplate]: The list of retrieved record objects with pagination info.
    """
    query = db.query(record_template_model.RecordTemplate).filter(
        record_template_model.RecordTemplate.user_id == user_id
    )

    total = query.count()

    records = (
        query.order_by(
            desc(getattr(record_template_model.RecordTemplate, "created_at"))
        )
        .offset(page_params.offset)
        .limit(page_params.size)
        .all()
    )

    record_template_schemas = [record.to_schema() for record in records]
    page = page_params.offset // page_params.size + 1
    result = PageableResultDTO(
        total=total, page=page, size=page_params.size, data=record_template_schemas
    )

    return result


def update_record_template(
    record_template_id: str,
    record_template_update: record_template_schema.RecordTemplateUpdate,
    db: Session,
):
    """
    This function updates a record's details in the database.

    Args:
        record_template_id (str): The ID of the record to update.
        record_update (schemas.RecordUpdate): The new details of the record.
        db (Session): The DB session.

    Returns:
        models.Record: The updated record object.
    """
    record = (
        db.query(record_template_model.RecordTemplate)
        .filter(record_template_model.RecordTemplate.id == record_template_id)
        .first()
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record Template not found"
        )
    for var, value in vars(record_template_update).items():
        setattr(record, var, value) if value else None
    db.commit()
    db.refresh(record)
    return record


def delete_record_template(record_template_id: str, db: Session):
    """
    This function deletes a record from the database.

    Args:
        record_template_id (str): The ID of the record template to delete.
        db (Session): The DB session.

    Returns:
        str: A message indicating the record was deleted.
    """
    record_template = (
        db.query(record_template_model.RecordTemplate)
        .filter(record_template_model.RecordTemplate.id == record_template_id)
        .first()
    )
    if not record_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record Template not found"
        )
    db.delete(record_template)
    db.commit()
    return "Record Template deleted"
