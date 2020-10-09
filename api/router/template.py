from fastapi import Depends, APIRouter, HTTPException
from uuid import UUID

# models
from models.template import Template, UpdateTemplate

# utils
from utils.uuid import generate_uuid
from utils.ngram import make_ngrams


def get_template_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/{locale}/{topic}')
    async def get_mail_template(locale, topic):
        query = {'locale': locale, 'topic': topic}
        res = await database['templates'].find_one(query, {'_id': False})

        if res is not None:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='Mail template not found')

    @router.post('/{locale}/{topic}')
    async def post_mail_template(topic, locale, model: Template, user=Depends(
            authenticator.get_current_superuser)):
        d = dict(model)
        d['_id'] = generate_uuid()
        d['topic'] = topic
        d['locale'] = locale
        d['ngrams'] = make_ngrams([d['subject'], d['message']])

        res = await database['templates'].insert_one(d)

        if res.acknowledged:
            return UUID(bytes=res.inserted_id)
        else:
            raise HTTPException(
                status_code=400, detail='Mail template not created')

    @router.patch('/{hex}')
    async def patch_mail_template(hex, model: UpdateTemplate, user=Depends(
            authenticator.get_current_superuser)):
        try:
            uuid = UUID(hex=hex, version=4)
        except TypeError:
            raise HTTPException(
                status_code=404, detail='Mail template not found')

        d = dict(model)
        d['ngrams'] = make_ngrams([d['subject'], d['message']])
        document = {'$set': d}
        query = {'_id': uuid}

        res = await database['templates'].update_one(query, document)

        if res.modified_count > 0:
            return uuid
        else:
            raise HTTPException(
                status_code=400, detail='Error updating template')

    return router
