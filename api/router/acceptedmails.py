from fastapi import Depends, APIRouter, HTTPException

import pymongo
from uuid import UUID

# models

def add_boat_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('')
    async def post_boat(boat: Boat, user=Depends(
            authenticator.get_current_superuser)):
        res = await database['accepted_addresses'].insert_one(dict(boat))

        if res.acknowledged:
            return {'status': 'ok'}
        else:
            raise HTTPException(status_code=400, detail='No boat was created')

    return router



async def get_boat(uuid, database):
    filter = {
        '_id': False
    }
    query = { 'uuid': UUID(uuid) }
    res = await database['boats'].find_one(query, filter)

    if res is not None:
        return res
    else:
        return None
