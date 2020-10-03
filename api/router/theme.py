from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
from uuid import uuid4

import pymongo
import shutil
import os

# models
from models.theme import ThemeModel


def get_themes_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/default')
    async def get_default_theme(themes_model: ThemeModel = Depends()):
        query = await database['themes'].find_one({}, {'_id': 0})

        if query is not None:
            return query
        else:
            return themes_model

    @router.patch('/default', dependencies=[Depends(
        authenticator.get_current_superuser)])
    async def patch_default_theme(themes_model: ThemeModel):
        document = {'$set': dict(themes_model)}

        res = await database['themes'].update_one({}, document)

        if res.modified_count > 0:
            return {'detail': 'Theme was successfully updated'}
        else:
            return {'detail': 'Did not update theme propably no changes'}

    @router.get('/default/image')
    async def get_theme_image():
        sort = [('_id', pymongo.DESCENDING)]
        res = await database['images'].find({}).sort(sort).to_list(length=1)

        if len(res) > 0:
            filename = res[0]['image']
        else:
            raise HTTPException(status_code=404, detail='Image was not found')

        if os.path.isfile(f'./static/{filename}'):
            return FileResponse(f'./static/{filename}', media_type='image/png')

        raise HTTPException(status_code=404, detail='Image was not found')

    @router.post('/default/image', dependencies=[Depends(
        authenticator.get_current_superuser)])
    async def post_theme_image(image: UploadFile = File(...)):
        filename = f'{uuid4()}.png'

        try:
            with Path(f'./static/{filename}').open('wb') as buffer:
                shutil.copyfileobj(image.file, buffer)
        finally:
            image.file.close()

            query = {'image': filename}
            res = await database['images'].insert_one(query)

            if res.acknowledged:
                return {'detail': 'Uploaded logo', 'image': filename}
            else:
                return {'detail': 'Upload error occured'}

    return router
