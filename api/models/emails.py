from bson.binary import Binary
from pydantic import BaseModel
from typing import List


class Emails(BaseModel):
    emails: List[str]
