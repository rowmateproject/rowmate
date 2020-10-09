from fastapi import Depends, APIRouter, HTTPException
from uuid import UUID

# models
from models.template import Template, UpdateTemplate

# utils
from utils.uuid import generate_uuid
from utils.ngram import make_ngrams


def get_templates_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/')
    async def get_template(user=Depends(
            authenticator.get_current_superuser)):
        filter = {'ngrams': False}
        docs = await database['templates'].count_documents({})
        res = await database['templates'].find({}, filter).to_list(length=docs)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No mail templates found')

    return router


def get_template_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.delete('/{hex}')
    async def delete_template(hex, user=Depends(
            authenticator.get_current_superuser)):
        try:
            req_uuid = UUID(hex=hex, version=4)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=404, detail='Invalid identifier')

        query = {'_id': req_uuid}
        res = await database['templates'].delete_one(query)

        if res.deleted_count > 0:
            return True
        else:
            raise HTTPException(
                status_code=404, detail='Mail template not found')

    @router.get('/{locale}/{topic}')
    async def get_templates(locale, topic):
        query = {'locale': locale, 'topic': topic}
        res = await database['templates'].find_one(query, {'_id': False})

        if res is not None:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='Mail template not found')

    @router.post('/{locale}/{topic}')
    async def post_template(topic, locale, model: Template, user=Depends(
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
    async def patch_template(hex, model: UpdateTemplate, user=Depends(
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
