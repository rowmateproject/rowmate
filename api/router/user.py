from fastapi import Depends, APIRouter, HTTPException

import pymongo
from uuid import UUID


async def get_user(uuid, database):
    filter = {
        '_id': False,
        'id': True,
        'avatar': True,
        'name': True,
        'email': True
    }
    query = { 'id': UUID(uuid) }
    res = await database['users'].find_one(query, filter)

    if res is not None:
        return res
    else:
        return None
