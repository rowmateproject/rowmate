from pydantic import BaseModel
from bson.binary import Binary
from datetime import datetime


class Address(BaseModel):
    created_at: datetime = datetime.utcnow()
    _id: Binary
    zip_code: str
    street_name: str
    house_number: str
    country_code: str
    location: str
    name: str


class UpdateAddress(Address):
    modified_at: datetime = datetime.utcnow()


class RequestAddress(BaseModel):
    zip_code: str
    street_name: str
    house_number: str
    country_code: str
    location: str
    name: str
