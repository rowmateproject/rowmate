from typing import Dict, Optional
from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime


class Translation(BaseModel):
    _id: Binary
    created_at: datetime = datetime.utcnow()
    translation: Dict[str, Dict[str, str]]
    lang: str


class UpdateTranslation(Translation):
    modified_at: datetime = datetime.utcnow()


class RequestTranslation(BaseModel):
    textarea: Optional[Dict[str, str]]
    input: Optional[Dict[str, str]]
