from bson.binary import Binary
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# enums
from enums.boatcategory import BoatCategoryEnum
from enums.discipline import DisciplineEnum
from enums.coxswain import CoxswainEnum


class Boat(BaseModel):
    id: Binary
    name: str
    crewsize: int
    added: datetime = datetime.utcnow()
    category: BoatCategoryEnum
    coxswain: CoxswainEnum
    discipline: DisciplineEnum
    manufacturer: Optional[str]
    built: Optional[int]
