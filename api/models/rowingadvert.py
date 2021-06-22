from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import UUID4
from uuid import uuid4
from datetime import datetime


class RowingAdvert(BaseModel):
    _id: Binary
    uuid: UUID4 = uuid4()
    created_at: datetime = datetime.now()
    creator: Optional[UUID4] # gets replaced in router
    time: Optional[datetime]
    boat: Optional[UUID4]
    text: str
