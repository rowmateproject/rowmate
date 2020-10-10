from pydantic import BaseModel, UUID4
from typing import List, Optional
from bson.binary import Binary
from datetime import datetime

# models
from models.address import Address


class Organization(Address, BaseModel):
    created_at: datetime = datetime.utcnow()
    address_id: Binary
    positions: Optional[List[UUID4]]


class UpdateOrganization(Organization):
    modified_at: datetime = datetime.utcnow()
