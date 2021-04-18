from pydantic import BaseModel, UUID4
from bson.binary import Binary
from datetime import datetime
from typing import List, Optional
from uuid import uuid4



class ChatMessage(BaseModel):
    created_at: datetime = datetime.utcnow()
    uuid: UUID4
    author: UUID4
    chat: UUID4
    content: str


class AddChatMessage(BaseModel):
    created_at: datetime = datetime.utcnow()
    _id: Binary
    uuid: UUID4 = uuid4()
    author: UUID4 = uuid4() # changed in router
    chat: UUID4
    content: str


class GetChatMessages(BaseModel):
    uuid: UUID4
