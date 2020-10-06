from pydantic import BaseModel
from typing import List


class RequestVote(BaseModel):
    reply: List[str]
