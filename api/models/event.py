from typing import Dict, List, Optional
from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    event_time: Optional[datetime]
    end_time: Optional[datetime]
    start_time: datetime
    min_participants: int
    max_participants: int
    repeat_interval: int
    contact_person: str
    repeat_unit: str
    location: str

    # store translations
    titles: Dict[str, Dict[str, str]]
    descriptions: Dict[str, Dict[str, str]]

    # if boats is empty, max_participants has to be used
    boats: List[Binary] = []

    # if empty, all members can sign up.
    allowed_memberclasses: List[Binary] = []

    # if equals 0, signup is not restricted
    # signup_from: timedelta = timedelta(seconds=0)


class UpdateEvent(Event):
    modified_at: datetime = datetime.utcnow()
