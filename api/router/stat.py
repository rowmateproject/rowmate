from fastapi import Depends, HTTPException, APIRouter
from datetime import datetime


def get_stats_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/dashboard')
    async def stats_dashboard(user=Depends(
            authenticator.get_current_active_user)):
        users = await database['users'].count_documents({'is_active': True})
        rowingads = await database['rowingadverts'].count_documents({
            'time': {'$gte': datetime.utcnow()}})
        events = await database['events'].count_documents({
            'event_time': {'$gte': datetime.utcnow()}})

        if users or events or rowingads:
            return {'users': users, 'events': events, 'rowingads': rowingads}
        else:
            raise HTTPException(
                status_code=404, detail='No stats were not found')

    @router.get('/votes')
    async def stats_vote(user=Depends(
            authenticator.get_current_active_user)):
        query = [{'$project': {'_id': 1, 'option_id': '$option_id',
                               'question_id': '$question_id',
                               'count_votes': {'$size': '$votes'}}},
                 {'$group': {'_id': {'grouped_questions': '$question_id'},
                             'count': {'$sum': '$count_votes'}, 'data':
                             {'$push': '$$ROOT'}}},
                 {'$unwind': {'path': '$data'}},
                 {'$lookup': {'from': 'questions',
                              'localField': 'data.question_id',
                              'foreignField': '_id', 'as': 'a'}},
                 {'$unwind': {'path': '$a'}},
                 {'$unwind': {'path': '$data.option_id'}},
                 {'$project': {'_id': 0, 'question': '$a.question', 'label':
                               {'$filter': {'input': '$a.forms', 'as': 'item',
                                            'cond':
                                            {'$eq': ['$$item.id',
                                                     '$data.option_id']}}},
                               'percentage':
                               {'$floor': {'$multiply':
                                           [{'$divide': [100, '$count']},
                                            '$data.count_votes']}}}},
                 {'$unwind': {'path': '$label',
                              'preserveNullAndEmptyArrays': True}},
                 {'$group': {'_id': '$question', 'results':
                             {'$push': {'label': '$label.value',
                                        'percentage': '$percentage'}}}}]

        docs = await database['answers'].count_documents({})
        res = await database['answers'].aggregate(query).to_list(length=docs)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(
                status_code=404, detail='No votes were not found')

    return router
