from datetime import datetime, timezone
from typing import Annotated
from pydantic import AfterValidator, BaseModel, Field, validator


def format_datetime_as_utc(value: datetime) -> str:
    """
    This validator ensures that the 'start_time' and 'end_time' fields are in UTC format.
    If the datetime is naive (i.e., it has no timezone information), it treats the datetime as UTC.
    It then returns the datetime in ISO 8601 format, replacing '+00:00' with 'Z' to indicate UTC.
    Args:
        value (datetime): The datetime value to be validated and formatted.

    Returns:
        str: The datetime value formatted in ISO 8601 format.
    """
    # Ensure the datetime is in UTC
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        # Treat naive datetime as UTC
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat().replace("+00:00", "Z")


UtcDatetime = Annotated[datetime, AfterValidator(format_datetime_as_utc)]


class BaseRecord(BaseModel):
    start_time: UtcDatetime
    end_time: UtcDatetime
    title: str = Field(max_length=100)
    note: str | None = Field(None, max_length=500)
    focus: int
    point: int


class RecordCreate(BaseRecord):
    pass


class RecordUpdate(BaseRecord):
    pass


class Record(BaseRecord):
    id: str
    created_at: datetime
