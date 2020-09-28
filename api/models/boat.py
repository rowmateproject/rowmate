from pydantic import BaseModel
from typing import Optional
from enums.boatcategory import BoatCategoryEnum
from enums.coxswain import CoxswainEnum
from enums.discipline import DisciplineEnum

class Boat(BaseModel):
    name: str
    crewsize: int
    category: BoatCategoryEnum
    coxswain: CoxswainEnum
    discipline: DisciplineEnum
    built: Optional[int]
    manufacturer: Optional[str]
