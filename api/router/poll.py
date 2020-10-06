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
        # query = {'translation': lang}
        docs = await database['polls'].count_documents({})
        res = await database['polls'].find({}).to_list(length=docs)

        if len(res) > 0:
            p = []

            for id in [r['questions'] for r in res]:
                filter = {'ngrams': False}
                query = {'_id': {'$in': id}}

                docs = await database['questions'].count_documents(query)
                res1 = await database['questions'].find(
                    query, filter).to_list(length=docs)

                query = {'question_id': {'$in': [r['_id'] for r in res1]}}
                docs = await database['votes'].count_documents(query)
                res2 = await database['votes'].find(query).to_list(length=docs)

                p.append(sorted([{**x, **{'reply': k['reply'] for k in res2
                                          if x['_id'] == k['question_id']}}
                                 for x in res1], key=lambda k: k['question']))

            return p
        else:
            raise HTTPException(status_code=404, detail='Polls not found')

    return router


def get_poll_router(database, authenticator) -> APIRouter:
    router = APIRouter()

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
