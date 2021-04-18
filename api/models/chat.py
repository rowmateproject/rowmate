from pydantic import BaseModel, UUID4
from bson.binary import Binary
from datetime import datetime
from typing import List, Optional
from uuid import uuid4



class Chat(BaseModel):
    created_at: datetime = datetime.utcnow()
    uuid: UUID4
    members: List[UUID4]
    owner: UUID4


class AddChat(BaseModel):
    created_at: datetime = datetime.utcnow()
    _id: Binary
    uuid: UUID4 = uuid4()
    members: List[UUID4]
    owner: UUID4 = uuid4() # gets replaced in router
