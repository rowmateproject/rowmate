from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


class Question(BaseModel):
    _id: Binary
    created_at: datetime = datetime.utcnow()
    forms: List[Dict[str, str]]
    question: str
    type: str


class UpdateQuestion(Question):
    modified_at: datetime = datetime.utcnow()


class RequestQuestion(BaseModel):
    forms: List[Dict[str, str]]
    question: str
    type: str


class LookupQuestion(BaseModel):
    query: str
