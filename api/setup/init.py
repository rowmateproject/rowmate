from datetime import datetime
from bson.binary import Binary
from polib import pofile

import os

# models
from models.translation import Translation, UpdateTranslation

# utils
from utils.uuid import generate_uuid


async def setup_translations(database):
    files = os.listdir('./setup/translations')

    for file in files:
        po = pofile(f'./setup/translations/{file}')
        lang = file.split('.')[1]

        r = [{x.msgid: x.msgstr, 'type': 'textarea'} if len(
            x.msgstr) > 32 else {
            x.msgid: x.msgstr, 'type': 'input'} for x in po]

        translation_doc: UpdateTranslation = {}
        translation_doc['modified_at']: datetime = datetime.utcnow()
        translation_doc['translation'] = r

        query = {'lang': lang}
        document = {'$set': translation_doc}

        res = await database['translations'].update_one(query, document)

        if res.modified_count == 0:
            uuid: Binary = generate_uuid()
            created_at: datetime = datetime.utcnow()
            translation_doc: Translation = {
                '_id': uuid,
                'created_at': created_at,
                'translation': r,
                'lang': lang
            }

            await database['translations'].insert_one(translation_doc)
