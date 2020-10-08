from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    poll_id: Optional[str]
    event_time: Optional[datetime]
    end_time: Optional[datetime]
    start_time: datetime
    min_participants: int
    max_participants: int
    repeat_interval: int
    repeat_unit: str

    # TODO: should be type of uuid later on
    contact_person: str

    # TODO: should be type of location with lat lng
    location: str

    # TODO: should be type of uuid later on
    author: Optional[str]

    # store translations
    titles: Dict[str, Dict[str, str]]
    descriptions: Dict[str, Dict[str, str]]

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
