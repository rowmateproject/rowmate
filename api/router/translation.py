from fastapi import Depends, APIRouter, HTTPException
from bson.binary import Binary
from datetime import datetime

# models
from models.translation import (
    Translation, RequestTranslation, UpdateTranslation)

# utils
from utils.uuid import generate_uuid


def get_translation_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/{lang}')
    async def get_translation(lang):
        query = {'lang': lang}
        filter = {'_id': False, 'lang': False}

        docs = await database['translations'].count_documents(query)
        res = await database['translations'].find(
            query, filter).to_list(length=docs)

        if len(res) > 0:
            t = {k: v for d in res[0]['translation'] for k, v in d.items(
            ) if d['type'] == 'textarea' and k != 'type'}
            i = {k: v for d in res[0]['translation'] for k, v in d.items(
            ) if d['type'] == 'input' and k != 'type'}

            return {'input': i, 'textarea': t}
        else:
            raise HTTPException(
                status_code=404, detail='No translations found')

    @router.post('/{lang}')
    async def post_translation(lang, model: RequestTranslation, user=Depends(
            authenticator.get_current_superuser)):
        query = {'lang': lang}
        docs = await database['translations'].count_documents(query)
        res = await database['translations'].find(query).to_list(length=docs)

        i = model.input
        t = model.textarea
        l1 = [{x[0]: x[1], 'type': 'textarea'} if len(
            x[1]) > 32 else {x[0]: x[1], 'type': 'input'} for x in i.items()]
        l2 = [{x[0]: x[1], 'type': 'textarea'} if len(
            x[1]) > 32 else {x[0]: x[1], 'type': 'input'} for x in t.items()]

        if len(res) == 0:
            uuid: Binary = generate_uuid()
            created_at: datetime = datetime.utcnow()

            translation_doc: Translation = {
                '_id': uuid,
                'created_at': created_at,
                'translation': l1 + l2,
                'lang': lang
            }

            res = await database['translations'].insert_one(translation_doc)

            if res.acknowledged:
                return {'detail': 'Translation was created'}
            else:
                raise HTTPException(
                    status_code=400, detail='Error creating translation')

        translation_doc: UpdateTranslation = {}
        translation_doc['modified_at']: datetime = datetime.utcnow()
        translation_doc['translation'] = l1 + l2

        query = {'lang': lang}
        document = {'$set': translation_doc}

        res = await database['translations'].update_one(query, document)

        if res.acknowledged:
            return {'detail': 'Updated translation translation'}
        else:
            raise HTTPException(
                status_code=400, detail='Error creating translation')

    return router
