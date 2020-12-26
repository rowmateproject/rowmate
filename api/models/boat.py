from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import UUID4
from uuid import uuid4
# enums
from enums.boatcategory import BoatCategoryEnum
from enums.discipline import DisciplineEnum
from enums.coxswain import CoxswainEnum


class Boat(BaseModel):
    _id: Binary
    uuid: str = uuid4()
    name: str
    crewsize: int
    added: datetime = datetime.utcnow()
    category: BoatCategoryEnum
    coxswain: CoxswainEnum
    discipline: DisciplineEnum
    manufacturer: Optional[str]
    built: Optional[int]


class LookupBoat(BaseModel):
    name: str
