from fastapi_users.models import (
    BaseUser, BaseUserDB, BaseUserCreate, BaseUserUpdate,
    BaseOAuthAccountMixin)
from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime


class User(BaseUser, BaseOAuthAccountMixin):
    is_active: bool = False
    is_accepted: bool = False
    is_confirmed: bool = False
    birth: Optional[datetime]
    locale: Optional[str]
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
    birth: Optional[datetime]
    avatar: Optional[dict]
    locale: Optional[str]
    phone: Optional[str]


class UserDB(User, BaseUserDB):
    pass


class UserList(BaseModel):
    mails: List[str] = []
    sendmail: bool = False


class LookupUser(BaseModel):
    name: str
