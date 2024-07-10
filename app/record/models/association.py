from sqlalchemy import Table, Column, String, ForeignKey
from app.config.database import DBBase

tag_record_association = Table(
    "tag_record",
    DBBase.metadata,
    Column("tag_id", String(36), ForeignKey("tags.id")),
    Column("record_id", String(36), ForeignKey("records.id")),
)

tag_record_template_association = Table(
    "tag_record_template",
    DBBase.metadata,
    Column("tag_id", String(36), ForeignKey("tags.id")),
    Column("record_template_id", String(36), ForeignKey("record_templates.id")),
)
