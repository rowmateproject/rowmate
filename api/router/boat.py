from fastapi import Depends, APIRouter, HTTPException

import pymongo
from uuid import UUID

# models
from models.boat import Boat


def get_boats_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('')
    async def get_all_boats(user=Depends(
            authenticator.get_current_active_user)):
        sort = [('_id', pymongo.DESCENDING)]
        filter = {'_id': False}

        res = await database['boats'].find(
            {}, filter).sort(sort).to_list(length=150)

        if res is not None:
            return res
        else:
            raise HTTPException(status_code=404, detail='No boats were found')

    return router




def delete_boat_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.delete('/{uuid}')
    async def delete_boat(uuid, user=Depends(
            authenticator.get_current_superuser)):
        query = { 'uuid': UUID(uuid) }
        res = await database['boats'].delete_one(query)
        if res.deleted_count > 0:
            return True
        else:
            raise HTTPException(
                status_code=404, detail='Boat was not found')

    return router


def add_boat_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('')
    async def post_boat(boat: Boat, user=Depends(
            authenticator.get_current_superuser)):
        res = await database['boats'].insert_one(dict(boat))

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
