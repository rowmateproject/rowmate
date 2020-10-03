from fastapi import Depends, APIRouter, HTTPException
from bson.binary import Binary
from datetime import datetime
from uuid import UUID

import pymongo

# models
from models.subscription import Subscription

# utils
from utils.uuid import generate_uuid


def get_subscription_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/events/{lang}')
    async def get_subscribed_events(lang, user=Depends(
            authenticator.get_current_active_user)):
        query = {'user_id': user.id}

        res = await database['subscriptions'].find(query).to_list(length=150)

        if len(res) == 0:
            raise HTTPException(
                status_code=404, detail='No subscriptions found')

        query = {
            '_id': {'$in': [x['events'] for x in res][0]},
            'event_time': {'$gte': datetime.utcnow()}
        }

        sort = [('event_time', pymongo.ASCENDING)]

        filter = {'_id': True,
                  f'titles.{lang}.title': True,
                  f'descriptions.{lang}.description': True,
                  'max_participants': True,
                  'min_participants': True,
                  'repeat_interval': True,
                  'contact_person': True,
                  'repeat_unit': True,
                  'modified_at': True,
                  'created_at': True,
                  'event_time': True,
                  'start_time': True,
                  'end_time': True,
                  'location': True}

        res = await database['events'].find(
            query, filter).sort(sort).to_list(length=150)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No subscriptions found')

    @router.post('/event/{hex}')
    async def post_subscribe_event(hex, user=Depends(
            authenticator.get_current_superuser)):
        try:
            req_uuid = UUID(hex=hex, version=4)
        except TypeError:
            raise HTTPException(status_code=404, detail='Event was not found')

        query = {'user_id': user.id}
        res = await database['subscriptions'].find(query).to_list(length=150)

        if len(res) == 0:
            uuid: Binary = generate_uuid()
            created_at: datetime = datetime.utcnow()

            subscription_doc: Subscription = {
                '_id': uuid,
                'user_id': user.id,
                'created_at': created_at,
                'events': [req_uuid]
            }

            res = await database['subscriptions'].insert_one(subscription_doc)

            if res.acknowledged:
                return {'detail': 'Subscription was created'}
            else:
                raise HTTPException(
                    status_code=400, detail='Error creating subscription')

        subscription_doc: Subscription = {}
        subscription_doc['modified_at']: datetime = datetime.utcnow()

        document = {'$set': subscription_doc,
                    '$addToSet': {'events': req_uuid}}
        query = {'user_id': user.id}

        res = await database['subscriptions'].update_one(query, document)

        if res.acknowledged:
            return {'detail': 'Updated event subscription'}
        else:
            raise HTTPException(
                status_code=400, detail='Error creating subscription')

    return router
