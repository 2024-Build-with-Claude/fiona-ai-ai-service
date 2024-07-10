from datetime import datetime
from pydantic import BaseModel, Field, UUID4


class TagBase(BaseModel):
    name: str = Field(..., max_length=100)


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class Tag(TagBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
