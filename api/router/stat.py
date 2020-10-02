from fastapi import Depends, HTTPException, APIRouter
from datetime import datetime

# models
from models.stat import StatsDashboard


def get_stats_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/dashboard',
                response_model=StatsDashboard,
                dependencies=[Depends(authenticator.get_current_active_user)])
    async def stats_dashboard():
        users = await database['users'].count_documents({'is_active': True})
        events = await database['events'].count_documents({
            'event_time': {'$gte': datetime.utcnow()}})

        if users or events:
            return {'users': users, 'events': events}
        else:
            raise HTTPException(
                status_code=404, detail='No stats were not found')

    return router
