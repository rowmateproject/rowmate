from bson.binary import Binary, UUID_SUBTYPE
from typing import Dict, Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4, UUID


class Event(BaseModel):
    id: Binary = Binary(bytes(bytearray(uuid4().bytes)), UUID_SUBTYPE)
    location: str
    start_time: datetime
    end_time: Optional[datetime]
    created_at: datetime = datetime.utcnow()
    min_participants: str
    max_participants: str
    contact_person: str

    # store translations
    titles: Dict[str, Dict[str, str]]
    descriptions: Dict[str, Dict[str, str]]

    # if boats is empty, max_participants has to be used
    boats: List[UUID] = []

    # if empty, all members can sign up.
    allowed_memberclasses: List[UUID] = []

    # if equals 0, signup is not restricted
    # signup_from: timedelta = timedelta(seconds=0)


class UpdateEvent(BaseModel):
    location: str
    start_time: datetime
    modified_at: datetime = datetime.utcnow()
    end_time: Optional[datetime]
    min_participants: str
    max_participants: str
    contact_person: str

    # store translations
    titles: Dict[str, Dict[str, str]]
    descriptions: Dict[str, Dict[str, str]]

    # if boats is empty, max_participants has to be used
    boats: List[UUID] = []

    # if empty, all members can sign up.
    allowed_memberclasses: List[UUID] = []

    # if equals 0, signup is not restricted
    # signup_from: timedelta = timedelta(seconds=0)
