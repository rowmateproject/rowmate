from bson.binary import Binary, UUID_SUBTYPE
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4


class TemplateModel(BaseModel):
    id: Binary = Binary(bytes(bytearray(uuid4().bytes)), UUID_SUBTYPE)
    locale: Optional[str]
    topic: Optional[str]
    subject: str
    message: str


class UpdateTemplateModel(TemplateModel):
    subject: str
    message: str
