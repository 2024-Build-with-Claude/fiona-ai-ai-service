from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.infrastructure.dependencies import get_pageable_param
from app.infrastructure.schemas import PageableParamDTO, PageableResultDTO
from app.record.schemas import record_template_schema
from app.record.services import record_template_service
from app.user.models import User
from app.user.services import get_current_user_base_on_config

router = APIRouter()


@router.post("", response_model=record_template_schema.RecordTemplate)
def create_record_template(
    template_data: record_template_schema.RecordTemplateCreate,
    user: User = Depends(get_current_user_base_on_config),
    db: Session = Depends(get_db),
):
    return record_template_service.create_record_template(
        template=template_data, user_id=user.id, db=db
    )


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=PageableResultDTO[record_template_schema.RecordTemplate],
)
def record_template_list(
    page_params: PageableParamDTO = Depends(get_pageable_param),
    user: User = Depends(get_current_user_base_on_config),
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of record templates with pagination and optional time range filtering.

    Args:
        page_params (PageableParamDTO): The pagination parameters.
        db (Session): The database session.

    Returns:
        PageableResultDTO[record_template_schema.RecordTemplate]: The list of records.
    """
    return record_template_service.get_record_templates(
        page_params=page_params,
        user_id=user.id,
        db=db,
    )


@router.get("/{template_id}", response_model=record_template_schema.RecordTemplate)
def get_record_template(template_id: str, db: Session = Depends(get_db)):
    template = record_template_service.get_record_template(template_id, db)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put(
    path="/{template_id}",
    status_code=status.HTTP_200_OK,
    response_model=record_template_schema.RecordTemplate,
)
def update_record(
    template_id: str,
    record_update: record_template_schema.RecordTemplateUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a record template.
    """
    # Call the service function to update the record
    updated_record_template = record_template_service.update_record_template(
        record_template_id=template_id, record_template_update=record_update, db=db
    )
    if not updated_record_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The record template with this id does not exist in the system",
        )
    return updated_record_template


@router.delete(
    path="/{template_id}",
    status_code=status.HTTP_200_OK,
)
def delete_record_template(
    template_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a record template.
    """
    # Call the service function to delete the record
    message = record_template_service.delete_record_template(
        record_template_id=template_id, db=db
    )
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The record template with this id does not exist in the system",
        )
    return {"message": message}
