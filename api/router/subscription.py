from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime

import pymongo


def get_subscription_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/events/{lang}')
    async def get_subscribed_events(lang, user=Depends(
            authenticator.get_current_active_user)):
        # TODO: remove mock data and create real subscription entries
        query = {'event_time': {'$gte': datetime.utcnow()}}
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

    return router
