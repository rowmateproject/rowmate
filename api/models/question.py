from typing import Optional, List, Dict
from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime


class Question(BaseModel):
    _id: Binary
    created_at: datetime = datetime.utcnow()
    forms: List[Dict[str, str]]
    question: str
    type: str


class UpdateQuestion(Question):
    modified_at: datetime = datetime.utcnow()


class RequestQuestion(BaseModel):
    forms: List[Optional[Dict[str, Optional[str]]]]
    question: str
    type: str


class LookupQuestion(BaseModel):
    query: str
