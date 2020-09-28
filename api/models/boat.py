from pydantic import BaseModel
from typing import Optional
from enums.boatcategory import BoatCategoryEnum
from enums.coxswain import CoxswainEnum
from enums.discipline import DisciplineEnum
from datetime import datetime
from bson.binary import Binary, UUID_SUBTYPE
from uuid import uuid4

class Boat(BaseModel):
    id: Binary = Binary(bytes(bytearray(uuid4().bytes)), UUID_SUBTYPE)
    name: str
    crewsize: int
    added: datetime = datetime.now()
    category: BoatCategoryEnum
    coxswain: CoxswainEnum
    discipline: DisciplineEnum
    built: Optional[int]
    manufacturer: Optional[str]
