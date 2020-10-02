from fastapi import Depends, APIRouter, HTTPException

import pymongo

# models
from models.boat import Boat


def get_boats_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/')
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


def get_boat_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('/')
    async def post_boat(boat: Boat, user=Depends(
            authenticator.get_current_superuser)):
        res = await database['boats'].insert_one(dict(boat))

        if res.acknowledged:
            return {'status': 'ok'}
        else:
            raise HTTPException(status_code=400, detail='No boat was created')

    return router
