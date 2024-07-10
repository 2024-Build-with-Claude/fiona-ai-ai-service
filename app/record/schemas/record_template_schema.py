from datetime import datetime
from pydantic import BaseModel, Field


class RecordTemplateBase(BaseModel):
    default_title: str = Field(..., max_length=100)
    default_focus: int
    default_point: int
    default_note: str | None = Field(None, max_length=500)


class RecordTemplateCreate(RecordTemplateBase):
    pass


class RecordTemplateUpdate(RecordTemplateBase):
    pass


class RecordTemplate(RecordTemplateBase):
    id: str
    created_at: datetime
