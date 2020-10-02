from fastapi import Depends, APIRouter, HTTPException
from uuid import UUID

# models
from models.template import TemplateModel, UpdateTemplateModel


def get_mail_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/{locale}/{topic}')
    async def get_mail_template(locale, topic):
        query = {'locale': locale, 'topic': topic}
        res = await database['mails'].find_one(query, {'_id': False})

        if res is not None:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='Mail template not found')

    @router.post('/{locale}/{topic}')
    async def post_mail_template(topic: str, locale: str, model: TemplateModel,
                                 user=Depends(
                                     authenticator.get_current_superuser)):
        object = dict(model)
        object['locale'] = locale
        object['topic'] = topic

        res = await database['mails'].insert_one(object)

        if res.acknowledged:
            return {'detail': 'Mail template was created',
                    'id': UUID(bytes=object['id'])}
        else:
            raise HTTPException(
                status_code=400, detail='Mail template not created')

    @router.patch('/{hex}')
    async def patch_mail_template(hex: str, model: UpdateTemplateModel,
                                  user=Depends(
                                      authenticator.get_current_superuser)):
        try:
            uuid = UUID(hex=hex, version=4)
        except TypeError:
            raise HTTPException(
                status_code=404, detail='Mail template not found')

        query = {'id': uuid}
        document = {'$set': dict(model)}

        res = await database['mails'].update_one(query, document)

        if res.modified_count > 0:
            return {'detail': 'Mail template was updated'}
        else:
            raise HTTPException(status_code=204)

    return router
