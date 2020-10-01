from typing import List, Optional
from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime


class Calendar(BaseModel):
    created_at: datetime = datetime.utcnow()
    events: Optional[List[Binary]]
    end_time: Optional[datetime]
    start_time: datetime


class UpdateCalendar(Calendar):
    modified_at: datetime = datetime.utcnow()
    events: Optional[List[Binary]]
    end_time: Optional[datetime]
    start_time: datetime
