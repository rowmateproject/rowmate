from fastapi import Depends, APIRouter, HTTPException
from bson.binary import Binary
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
        inserted = []
        updated = []

        if d['reply'] == 'undefined':
            raise HTTPException(
                status_code=400, detail='Invalid option provided')

        document = {'$set': d}
        query = {'question_id': req_uuid,
                 'option_id': d['reply'][0], 'user_id': user.id}

        res = await database['votes'].update_one(query, document)

        if res.modified_count == 0:
            uuid: Binary = generate_uuid()

            d['_id'] = uuid
            d['question_id'] = req_uuid
            d['user_id'] = user.id

            res = await database['votes'].insert_one(d)

            if res.acknowledged:
                inserted.append(UUID(bytes=res.inserted_id))
        else:
            updated.append(req_uuid)

        if len(updated) > 0 or len(inserted) > 0:
            query = {'question_id': req_uuid, 'option_id': d['reply']}
            document = {'$set': {'option_id': d['reply']},
                        '$addToSet': {'votes': {'$each': inserted}}}

            res = await database['answers'].update_one(query, document)

            if res.modified_count == 0:
                uuid: Binary = generate_uuid()

                answer_doc = {
                    '_id': uuid,
                    'option_id': d['reply'],
                    'question_id': req_uuid,
                    'votes': inserted
                }

                await database['answers'].insert_one(answer_doc)

            return d['reply']
        else:
            raise HTTPException(status_code=400, detail='Answer not updated')

    return router
