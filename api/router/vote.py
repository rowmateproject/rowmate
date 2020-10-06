from fastapi import Depends, APIRouter, HTTPException
from uuid import UUID

# models
from models.vote import RequestVote

# utils
from utils.uuid import generate_uuid


def get_vote_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.patch('/{hex}')
    async def patch_vote(hex, model: RequestVote, user=Depends(
            authenticator.get_current_active_user)):
        try:
            req_uuid = UUID(hex=hex, version=4)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=404, detail='Invalid identifier')

        d = dict(model)
        document = {'$set': d}
        query = {'question_id': req_uuid, 'user_id': user.id}

        res = await database['votes'].update_one(query, document)

        if res.modified_count == 0:
            d = dict(model)
            d['_id'] = generate_uuid()
            d['question_id'] = req_uuid
            d['user_id'] = user.id

            res = await database['votes'].insert_one(d)

            if res.acknowledged:
                return d['reply']
        else:
            return d['reply']

    return router
