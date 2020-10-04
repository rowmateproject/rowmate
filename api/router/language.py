from fastapi import File, Depends, APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from polib import pofile, POFile, POEntry
from bson.binary import Binary
from datetime import datetime
from pathlib import Path

import shutil
import os

# models
from models.translation import (
    Translation, RequestTranslation, UpdateTranslation)

# utils
from utils.uuid import generate_uuid


def get_language_router(database, authenticator) -> APIRouter:
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

    @router.post('/import/{lang}')
    async def import_translation(lang, file: UploadFile = File(...)):
        filename = f'import.{lang}.po'

        try:
            with Path(f'./static/{filename}').open('wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
        finally:
            file.file.close()
            po = pofile(f'./static/{filename}')
            r = [{x.msgid: x.msgstr, 'type': 'textarea'} if len(
                x.msgstr) > 32 else {
                x.msgid: x.msgstr, 'type': 'input'} for x in po]

            translation_doc: UpdateTranslation = {}
            translation_doc['modified_at']: datetime = datetime.utcnow()
            translation_doc['translation'] = r

            query = {'lang': lang}
            document = {'$set': translation_doc}

            res = await database['translations'].update_one(query, document)

            if res.acknowledged:
                return await get_translation(lang)
            else:
                raise HTTPException(
                    status_code=400, detail='Upload error occured')

    @router.get('/export/{lang}')
    async def export_translation(lang):
        filename = f'export.{lang}.po'
        query = {'lang': lang}

        docs = await database['translations'].count_documents(query)
        res = await database['translations'].find(query).to_list(length=docs)

        po = POFile()
        po.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'me@rowmate.org',
            'POT-Creation-Date': '2020-10-04 21:00+0200',
            'PO-Revision-Date': '2020-10-04 21:00+0200',
            'Last-Translator': 'Support <support@rowmate.org>',
            'Language-Team': 'English <support@rowmate.org>',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit'
        }

        if len(res) > 0:
            for value in res[0]['translation']:
                items = list(value.items())[0]

                entry = POEntry(
                    msgid=items[0],
                    msgstr=items[1]
                )

                po.append(entry)

        po.save(f'./static/{filename}')

        if os.path.isfile(f'./static/{filename}'):
            return FileResponse(f'./static/{filename}')

        raise HTTPException(status_code=404, detail='Translation not found')

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
