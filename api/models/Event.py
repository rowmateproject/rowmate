from pydantic import BaseModel

class Event(BaseModel):
    title: str
    description: str
