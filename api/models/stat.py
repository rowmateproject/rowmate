from pydantic import BaseModel


class StatsDashboard(BaseModel):
    events: int
    users: int
