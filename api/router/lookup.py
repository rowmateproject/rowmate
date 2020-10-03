from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime

import pymongo
import re

# models
from models.user import LookupUser
from models.subscription import LookupSubscription
from models.event import LookupEvent


def get_lookup_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('/events/{lang}')
    async def lookup_events(lang, event: LookupEvent, user=Depends(
            authenticator.get_current_active_user)):
        sort = [('score', {'$meta': 'textScore'})]
        filter = {'score': {'$meta': 'textScore'}}
        query = {'$text': {'$search': event.query, '$caseSensitive': False}}

        res = await database['events'].find(
            query, filter).sort(sort).to_list(length=15)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No events found')

    @router.post('/subscriptions/{lang}')
    async def lookup_subscriptions(lang, subscription: LookupSubscription,
                                   user=Depends(
                                       authenticator.get_current_active_user)):
        query = {'user_id': user.id}
        res = await database['subscriptions'].find(query).to_list(length=15)

        if len(res) == 0:
            raise HTTPException(
                status_code=404, detail='No subscriptions found')

        sort = [('score', {'$meta': 'textScore'})]
        filter = {'score': {'$meta': 'textScore'}}
        query = {
            '_id': {'$in': [x['events'] for x in res][0]},
            '$text': {'$search': subscription.query, '$caseSensitive': False},
            'event_time': {'$gte': datetime.utcnow()}
        }

        res = await database['events'].find(
            query, filter).sort(sort).to_list(length=15)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No subscriptions found')

    @router.post('/users')
    async def lookup_users(req: LookupUser, user=Depends(
            authenticator.get_current_active_user)):
        sort = [('_id', pymongo.DESCENDING)]
        query = {'name': {'$regex': re.compile(
            req.name, re.IGNORECASE)}, 'is_active': True}
        filter = {'_id': False, 'name': True, 'avatar': True}

        res = await database['users'].find(
            query, filter).sort(sort).to_list(length=15)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No users found')

    return router
