from fastapi import Depends, APIRouter, HTTPException, Response

import pymongo
from uuid import UUID
import re
# models
from models.emails import Emails

regex = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"

def add_emails_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('/add')
    async def post_emails(emails: Emails, response: Response, user=Depends(
            authenticator.get_current_superuser)):

        emailsdoc = []
        for email in emails.emails:
            print(re.search(regex, email))
            if re.search(regex, email):
                emailsdoc.append({'email':email})
            else:
                raise HTTPException(status_code=400, detail='Not all E-Mail-Addresses are valid')



        res = await database['accepted_emails'].insert_many(emailsdoc)

        if res.acknowledged:
            response.status_code = 201
            return {'status': 'ok'}
        else:
            raise HTTPException(status_code=400, detail='No emails were added')

    return router
