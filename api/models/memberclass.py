from pydantic import BaseModel, validator
from typing import Dict


maxtitlelength = 30


class MemberClass(BaseModel):
    description: Dict[str, str]
    title: Dict[str, str]

    @validator('title')
    def max_length(cls, v):
        lngs = []

        for key in v:
            if len(v[key]) > maxtitlelength:
                lngs.append(key)
        if len(lngs) != 0:
            raise ValueError(
                f'Title is too long for language(s) { ", ".join(lngs) }')

        return v
