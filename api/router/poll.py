from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime
from bson.binary import Binary
from typing import List, Dict
from uuid import UUID

# models
from models.question import Question, UpdateQuestion
from models.poll import RequestPoll

# utils
from utils.uuid import generate_uuid
from utils.ngram import make_ngrams


def get_polls_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/{lang}')
    async def get_polls(lang, user=Depends(
            authenticator.get_current_active_user)):
        query = [{'$unwind': '$questions'},
                 {'$lookup': {'from': 'questions', 'localField': 'questions',
                              'foreignField': '_id', 'as': 'a'}},
                 {'$unwind': {'path': '$a'}},
                 {'$project': {'_id': '$a._id', 'forms': '$a.forms',
                               'type': '$a.type', 'question': '$a.question'}},
                 {'$group': {'_id': {'_id': '$_id', 'type': '$type',
                                     'question': '$question'},
                             'forms': {'$push': '$forms'}}},
                 {'$unwind': {'path': '$forms'}},
                 {'$project': {'_id': '$_id._id', 'question': '$_id.question',
                               'type': '$_id.type', 'forms': '$forms'}},
                 {'$addFields': {'reply': []}}]

        docs = await database['polls'].count_documents({})
        res = await database['polls'].aggregate(query).to_list(length=docs)

        if len(res) > 0:
            return res
        else:
            raise HTTPException(status_code=404, detail='Polls not found')

    return router


def get_poll_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.delete('/{hex}')
    async def delete_poll(hex, user=Depends(
            authenticator.get_current_superuser)):
        try:
            req_uuid = UUID(hex=hex, version=4)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=404, detail='Invalid identifier')

        query = [{'$match': {'questions': {'$in': [req_uuid]}}},
                 {'$lookup': {'from': 'votes', 'localField': 'questions',
                              'foreignField': 'question_id', 'as': 'a'}},
                 {'$lookup': {'from': 'answers', 'localField': 'a._id',
                              'foreignField': 'votes', 'as': 'b'}},
                 {'$project': {'_id': False, 'poll_id': '$_id',
                               'answers': '$b._id', 'votes': '$a._id',
                               'questions': '$questions', }}]

        res = await database['polls'].aggregate(query).to_list(length=1)

        if len(res) > 0:
            for r in res[0]['answers']:
                await database['answers'].delete_one({'_id': r})

            for r in res[0]['votes']:
                await database['votes'].delete_one({'_id': r})

            for r in res[0]['questions']:
                await database['questions'].delete_one({'_id': r})

            query = {'_id': res[0]['poll_id']}
            await database['polls'].delete_one(query)

            return True
        else:
            raise HTTPException(
                status_code=404, detail='Mail poll not found')

    @router.post('')
    async def post_poll(model: RequestPoll, user=Depends(
            authenticator.get_current_superuser)):
        inserted = []

        for question in model.questions:
            uuid: Binary = generate_uuid()
            created_at: datetime = datetime.utcnow()
            ngram_forms = [x['value'] for x in question.forms if x]

            question_doc: Question = {
                '_id': uuid,
                'user_id': user.id,
                'created_at': created_at,
                'question': question.question,
                'forms': question.forms,
                'type': question.type,
                'ngrams': make_ngrams([question.question, ngram_forms])
            }

            res = await database['questions'].insert_one(question_doc)

            if res.acknowledged:
                inserted.append(UUID(bytes=res.inserted_id))

        if len(inserted) > 0:
            document = {'_id': generate_uuid(), 'questions': inserted}
            await database['polls'].insert_one(document)

    @router.patch('/{hex}')
    async def patch_poll(hex, model: RequestPoll, user=Depends(
            authenticator.get_current_superuser)):
        try:
            req_uuid = UUID(hex=hex, version=4)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=404, detail='Invalid identifier')

        updated = []

        for question in model.questions:
            ngram_forms = [x['value'] for x in question.forms if x]

            poll_doc: UpdateQuestion = {}
            poll_doc['modified_at']: datetime = datetime.utcnow()
            poll_doc['forms']: List[Dict[str, str]] = question.forms
            poll_doc['question']: str = question.question
            poll_doc['type']: str = question.type
            poll_doc['ngrams'] = make_ngrams([question.question, ngram_forms])

            query = {'_id': req_uuid}
            document = {'$set': poll_doc}

            res = await database['questions'].update_one(query, document)

            if res.acknowledged:
                updated.append(res.acknowledged)
            else:
                pass

        if len(updated) > 0:
            query = {'_id': req_uuid, 'questions': {'$in': updated}}
            document = {'$addToSet': {'questions': {'$each': updated}}}

            res = await database['polls'].update_one(query, document)

            if res.acknowledged:
                return {'detail': 'Updated poll'}

        raise HTTPException(status_code=400, detail='Error updating poll')

    return router
