from typing import List, Optional
from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime


class Subscription(BaseModel):
    created_at: datetime = datetime.utcnow()
    events: Optional[List[Binary]]


class UpdateSubscription(Subscription):
    modified_at: datetime = datetime.utcnow()
    events: Optional[List[Binary]]


class LookupSubscription(BaseModel):
    query: str
