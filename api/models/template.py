from pydantic import BaseModel
from typing import Optional


class Template(BaseModel):
    locale: Optional[str]
    topic: Optional[str]
    subject: str
    message: str


class UpdateTemplate(Template):
    _id: str


class LookupTemplate(BaseModel):
    query: str
