from pydantic import BaseModel
from typing import List

# models
from models.question import RequestQuestion


class RequestPoll(BaseModel):
    questions: List[RequestQuestion]
