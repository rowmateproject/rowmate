from pydantic import BaseModel

class Boat(BaseModel):
    name: str
    crewsize: int
