from bson.binary import Binary
from pydantic import BaseModel
from typing import Optional


class TemplateModel(BaseModel):
    id: Binary
    locale: Optional[str]
    topic: Optional[str]
    subject: str
    message: str


class UpdateTemplateModel(TemplateModel):
    subject: str
    message: str
