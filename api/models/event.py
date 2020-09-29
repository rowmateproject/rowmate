from bson.binary import Binary, UUID_SUBTYPE
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from .pydanticclasses.pydanticobjectid import PydanticObjectId
from pydantic import BaseModel
from uuid import uuid4


class Event(BaseModel):
    id: Binary = Binary(bytes(bytearray(uuid4().bytes)), UUID_SUBTYPE)
    created: datetime = datetime.utcnow()
    starttime: datetime
    max_participants: int = 0
    endtime: Optional[datetime]
    description: Dict[str, str]

    # store translations
    title: Dict[str, str]

    # if boats is empty, max_participants has to be used
    boats: List[PydanticObjectId] = []

    # if equals 0, signup is not restricted
    signupfrom: timedelta = timedelta(seconds=0)

    # if empty, all members can sign up.
    allowedmemberclasses: List[PydanticObjectId] = []
