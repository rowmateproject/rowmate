from fastapi_users.models import BaseUser, BaseUserDB, BaseUserCreate, BaseUserUpdate
from typing import Optional, List, Dict, Sequence, Type
from datetime import datetime
from pydantic import BaseModel
from fastapi_users.db import MongoDBUserDatabase, BaseUserDatabase

class User(BaseUser):
    is_active: bool = False
    is_accepted: bool = False
    is_confirmed: bool = False
    birth: Optional[datetime]
    phone: Optional[str]
    name: Optional[str]
    avatar: Dict = {
        'isCircle': True,
        'mouthType': 'Smile',
        'accessoriesType': 'Blank',
        'graphicType': 'Bat',
        'topType': 'Hat',
        'topColor': 'Gray02',
        'clotheType': 'CollarSweater',
        'clotheColor': 'Black',
        'eyeType': 'Wink',
        'eyebrowType': 'Default',
        'facialHairType': 'Blank',
        'facialHairColor': 'Auburn',
        'hairColor': 'Brown',
        'skinColor': 'Yellow',
        'circleColor': '#87CEEB'
    }


class UserCreate(BaseUserCreate):
    name: str


class UserUpdate(User, BaseUserUpdate):
    birth: datetime
    avatar: dict
    phone: str


class UserDB(User, BaseUserDB):
    pass


class UserList(BaseModel):
    mails: List[str] = []
    sendmail: bool = False


class FindUser(BaseModel):
    limit: int = 10
    name: str
