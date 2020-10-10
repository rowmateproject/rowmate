from pydantic import BaseModel
from bson.binary import Binary
from typing import List


class Position(BaseModel):
    _id: Binary
    member: str
    title: str


class RequestPosition(BaseModel):
    positions: List[Position]
