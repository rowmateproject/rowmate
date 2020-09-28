from pydantic import BaseModel, ValidationError, validator
from typing import Dict, Optional, List

maxtitlelength = 30
class MemberClass(BaseModel):
    title: Dict[str, str]
    description: Dict[str, str]

    @validator('title')
    def maxlength(cls, v):
        lngs = []
        for key in v:
            if len(v[key]) > maxtitlelength:
                lngs.append(key)
        if len(lngs) != 0:
            raise ValueError(f'Title is too long for language(s) { ", ".join(lngs) }')
        return v
