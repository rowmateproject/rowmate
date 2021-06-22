from fastapi import Depends, APIRouter, HTTPException

import pymongo
from uuid import UUID

# models
from models.rowingadvert import RowingAdvert
from .user import get_user
from .boat import get_boat

def get_rowingadverts_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('')
    async def get_all_rowingads(user=Depends(
            authenticator.get_current_active_user)):
        sort = [('_id', pymongo.DESCENDING)]
        filter = {'_id': False}

        res = await database['rowingadverts'].find(
            {}, filter).sort(sort).to_list(length=150)

        print(res)
        for i,entry in enumerate(res):
            if entry['creator'] is not None:
                userobj = await get_user(str(entry['creator']),database)
                if userobj is not None:
                    res[i]['creator'] = userobj

        if res is not None:
            return res
        else:
            raise HTTPException(status_code=404, detail='No rowing-adverts were found')

    return router


def get_rowingadvert_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/{uuid}')
    async def get_all_rowingads(uuid, user=Depends(
            authenticator.get_current_active_user)):
        filter = {'_id': False}
        query = { 'uuid': UUID(uuid) }
        res = await database['rowingadverts'].find_one(query, filter)

        if res is not None:
            userobj = await get_user(str(res['creator']),database)
            if userobj is not None:
                res['creator'] = userobj
            if res['boat'] != None:
                boatobj = await get_boat(str(res['boat']),database)
                if boatobj is not None:
                    res['boat'] = boatobj
            return res
        else:
            raise HTTPException(status_code=404, detail='No rowing-advert was found with this id')

    return router



def delete_rowingadvert_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.delete('/{uuid}')
    async def delete_rowingadvert(uuid, user=Depends(
            authenticator.get_current_user)):
        query = { 'uuid': UUID(uuid) }
        res = await database['rowingadverts'].find_one(query)
        if res["creator"] == user.id or user.is_superuser == True:
            res = await database['rowingadverts'].delete_one(query)
            if res.deleted_count > 0:
                return True
            else:
                raise HTTPException(
                    status_code=404, detail='Ad was not found')
        else:
            raise HTTPException(
                status_code=403, detail='Can\'t delete this ad')

    return router


def add_rowingadvert_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('')
    async def post_rowingadvert(advert: RowingAdvert, user=Depends(
            authenticator.get_current_user)):

        advert.creator = user.id
        res = await database['rowingadverts'].insert_one(dict(advert))

        if res.acknowledged:
            return {'status': 'ok'}
        else:
            raise HTTPException(status_code=400, detail='No advert was created')

    return router
