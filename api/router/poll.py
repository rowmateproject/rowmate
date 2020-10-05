from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime
from bson.binary import Binary
from typing import List, Dict
from uuid import UUID

# models
from models.poll import Poll, UpdatePoll, RequestPoll

# utils
from utils.uuid import generate_uuid
from utils.ngram import make_ngrams


def get_poll_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/latest/{lang}')
    async def get_latest_poll(lang, user=Depends(
            authenticator.get_current_active_user)):

        res = await database['polls'].find_one()

        if res is not None:
            return res
        else:
            raise HTTPException(status_code=404, detail='Poll not found')

    @router.post('')
    async def post_poll(model: RequestPoll, user=Depends(
            authenticator.get_current_superuser)):
        ngram_forms = [x['value'] for x in model.forms if x]

        uuid: Binary = generate_uuid()
        created_at: datetime = datetime.utcnow()

        poll_doc: Poll = {
            '_id': uuid,
            'user_id': user.id,
            'created_at': created_at,
            'translation': model.translation,
            'question': model.question,
            'forms': model.forms,
            'type': model.type,
            'ngrams': make_ngrams([model.question, ngram_forms])
        }

        print(poll_doc)

        res = await database['polls'].insert_one(poll_doc)

        if res.acknowledged:
            return UUID(bytes=res.inserted_id)
        else:
            raise HTTPException(
                status_code=400, detail='Error creating poll')

    @router.patch('/{hex}')
    async def patch_poll(hex, model: RequestPoll, user=Depends(
            authenticator.get_current_superuser)):
        try:
            req_uuid = UUID(hex=hex, version=4)
        except (TypeError, ValueError):
            req_uuid = None

        ngram_forms = [x['value'] for x in model.forms if x]

        poll_doc: UpdatePoll = {}
        poll_doc['modified_at']: datetime = datetime.utcnow()
        poll_doc['forms']: List[Dict[str, str]] = model.forms
        poll_doc['translation']: str = model.translation
        poll_doc['question']: str = model.question
        poll_doc['type']: str = model.type
        poll_doc['ngrams'] = make_ngrams([model.question, ngram_forms])

        query = {'_id': req_uuid}
        document = {'$set': poll_doc}

        res = await database['polls'].update_one(query, document)

        if res.acknowledged:
            return {'detail': 'Updated poll'}
        else:
            raise HTTPException(
                status_code=400, detail='Error updating poll')

    return router
