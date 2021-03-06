from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime

import pymongo
import re

# models
from models.user import LookupUser
from models.template import LookupTemplate
from models.subscription import LookupSubscription
from models.question import LookupQuestion
from models.event import LookupEvent
from models.boat import LookupBoat

def get_lookup_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('/events/{lang}')
    async def lookup_events(lang, event: LookupEvent, user=Depends(
            authenticator.get_current_active_user)):
        sort = [('score', {'$meta': 'textScore'})]
        filter = {'score': {'$meta': 'textScore'}, 'ngrams': False}
        query = {'$text': {'$search': event.query, '$caseSensitive': False}}

        res = await database['events'].find(
            query, filter).sort(sort).to_list(length=10)

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
        res = await database['subscriptions'].find(query).to_list(length=10)

        if len(res) == 0:
            raise HTTPException(
                status_code=404, detail='No subscriptions found')

        sort = [('score', {'$meta': 'textScore'})]
        filter = {'score': {'$meta': 'textScore'}, 'ngrams': False}
        query = {
            '_id': {'$in': [x['events'] for x in res][0]},
            '$text': {'$search': subscription.query, '$caseSensitive': False},
            'event_time': {'$gte': datetime.utcnow()}
        }

        res = await database['events'].find(
            query, filter).sort(sort).to_list(length=10)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No subscriptions found')

    @router.post('/question/{lang}')
    async def lookup_question(lang, model: LookupQuestion, user=Depends(
            authenticator.get_current_active_user)):
        query = [{'$match': {'$text': {'$search': model.query,
                                       '$caseSensitive': False}}},
                 {'$sort': {'score': {'$meta': 'textScore'}}},
                 {'$lookup': {'from': 'polls', 'localField': '_id',
                              'foreignField': 'questions', 'as': 'a'}},
                 {'$project': {'score': {'$meta': 'textScore'},
                               'question': '$question',
                               'forms': '$forms', 'type': '$type'}}]

        docs = await database['questions'].count_documents({})
        res = await database['questions'].aggregate(query).to_list(length=docs)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No questions found')

    @router.post('/template/{lang}')
    async def lookup_template(lang, model: LookupTemplate, user=Depends(
            authenticator.get_current_superuser)):
        sort = [('score', {'$meta': 'textScore'})]
        filter = {'score': {'$meta': 'textScore'}, 'ngrams': False}
        query = {'$text': {'$search': model.query, '$caseSensitive': False}}

        res = await database['templates'].find(
            query, filter).sort(sort).to_list(length=10)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No mail template found')

    @router.post('/users')
    async def lookup_users(req: LookupUser, user=Depends(
            authenticator.get_current_active_user)):
        sort = [('_id', pymongo.DESCENDING)]
        filter = {'_id': False, 'name': True, 'avatar': True}
        query = {'name': {'$regex': re.compile(
            req.name, re.IGNORECASE)}, 'is_active': True}

        if user.is_superuser is True:
            filter = {'_id': False, 'hashed_password': False}

        res = await database['users'].find(
            query, filter).sort(sort).to_list(length=10)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No users found')

    @router.post('/boats')
    async def lookup_boats(req: LookupBoat, user=Depends(
            authenticator.get_current_active_user)):
        sort = [('_id', pymongo.DESCENDING)]
        filter = {'_id': False}
        query = {'name': {'$regex': re.compile(
            req.name, re.IGNORECASE)}}

        res = await database['boats'].find(
            query, filter).sort(sort).to_list(length=10)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No boats found')

    return router
