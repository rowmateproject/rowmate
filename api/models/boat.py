from bson.binary import Binary, UUID_SUBTYPE
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import uuid4

# enums
from enums.boatcategory import BoatCategoryEnum
from enums.discipline import DisciplineEnum
from enums.coxswain import CoxswainEnum


class Boat(BaseModel):
    id: Binary = Binary(bytes(bytearray(uuid4().bytes)), UUID_SUBTYPE)
    name: str
    crewsize: int
    added: datetime = datetime.utcnow()
    category: BoatCategoryEnum
    coxswain: CoxswainEnum
    discipline: DisciplineEnum
    manufacturer: Optional[str]
    built: Optional[int]
