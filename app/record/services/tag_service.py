from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.record.models import tag_model
from app.record.schemas import tag_schema


def create_tag(tag: tag_schema.TagCreate, user_id: str, db: Session) -> tag_schema.Tag:
    new_tag = tag_model.Tag(name=tag.name, user_id=user_id)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


def get_tag(tag_id: str, db: Session) -> tag_schema.Tag:
    tag = db.query(tag_model.Tag).filter(tag_model.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


def get_tags_by_user(user_id: str, db: Session) -> list[tag_schema.Tag]:
    tags = db.query(tag_model.Tag).filter(tag_model.Tag.user_id == user_id).all()

    tag_schemas = [tag.to_schema() for tag in tags]

    return tag_schemas


def update_tag(
    tag_id: str, tag_data: tag_schema.TagCreate, db: Session
) -> tag_schema.Tag:
    tag = db.query(tag_model.Tag).filter(tag_model.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    tag.name = tag_data.name
    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(tag_id: str, db: Session) -> None:
    tag = db.query(tag_model.Tag).filter(tag_model.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    db.delete(tag)
    db.commit()
