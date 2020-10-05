from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


class Poll(BaseModel):
    _id: Binary
    created_at: datetime = datetime.utcnow()
    forms: List[Dict[str, str]]
    translation: str
    question: str
    type: str


class UpdatePoll(Poll):
    modified_at: datetime = datetime.utcnow()


class LookupPoll(BaseModel):
    query: str


class RequestPoll(BaseModel):
    forms: List[Dict[str, str]]
    translation: str
    question: str
    type: str
