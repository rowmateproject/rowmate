from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic import UUID4

class Event(BaseModel):
    end_time: Optional[datetime]
    start_time: datetime
    max_participants: int
    repeat_interval: int
    repeat_unit: str
    title: str
    description: str
    # TODO: should be type of location with lat lng
    location: str
    creator: Optional[UUID4] # gets replaced in route
    readaccess: List[UUID4] = []

    # if boats is empty, max_participants has to be used
    boats: List[str] = []

    # if empty, all members can sign up.
    allowed_memberclasses: List[str] = []

    # if equals 0, signup is not restricted
    # signup_from: timedelta = timedelta(seconds=0)


class UpdateEvent(Event):
    modified_at: datetime = datetime.utcnow()

    # TODO: should be type of uuid later on
    modified_by: Optional[str]


class LookupEvent(BaseModel):
    query: str
