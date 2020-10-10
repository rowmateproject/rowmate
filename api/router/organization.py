from fastapi import Depends, APIRouter, HTTPException
from bson.binary import Binary
from uuid import UUID

# models
from models.address import RequestAddress
from models.organization import Organization, UpdateOrganization

# utils
from utils.uuid import generate_uuid


def get_organization_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('')
    async def get_organization(user=Depends(
            authenticator.get_current_active_user)):
        query = [{'$lookup': {'from': 'addresses', 'localField':
                              'address_id', 'foreignField': '_id', 'as': 'a'}},
                 {'$unwind': {'path': '$a'}},
                 {'$project': {'_id': '$_id', 'name': '$a.name',
                               'street_name': '$a.street_name',
                               'house_number': '$a.house_number',
                               'zip_code': '$a.zip_code',
                               'country_code': '$a.country_code',
                               'location': '$a.location',
                               'name': '$a.name'}}]

        res = await database['organizations'].aggregate(
            query).to_list(length=1)

        if len(res) > 0:
            return res[0]
        raise HTTPException(
            status_code=404, detail='Organization not found')

    @router.post('')
    async def post_address(model: RequestAddress, user=Depends(
            authenticator.get_current_superuser)):
        address_uuid: Binary = generate_uuid()

        address_doc = dict(model)
        address_doc['_id'] = address_uuid

        res = await database['addresses'].insert_one(address_doc)

        if res.acknowledged:
            organization_uuid: Binary = generate_uuid()

            address_doc: Organization = {}
            address_doc['_id'] = organization_uuid
            address_doc['address_id'] = address_uuid

            res = await database['organizations'].insert_one(address_doc)

            if res.acknowledged:
                return UUID(bytes=res.inserted_id)
            raise HTTPException(
                status_code=400, detail='Organization not created')
        raise HTTPException(
            status_code=400, detail='Address not created')

    @router.patch('/{hex}')
    async def patch_address(hex, model: RequestAddress, user=Depends(
            authenticator.get_current_superuser)):
        try:
            req_uuid = UUID(hex=hex, version=4)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=404, detail='Invalid identifier')
        query = {'_id': req_uuid}

        res = await database['organizations'].find_one(query)

        if res is not None:
            address_doc: UpdateOrganization = dict(model)
            document = {'$set': address_doc}
            query = {'_id': {'$in': [res['address_id']]}}

            res = await database['addresses'].update_one(query, document)

            if res.modified_count > 0:
                return req_uuid
            else:
                raise HTTPException(
                    status_code=400, detail='Address not updated')
        else:
            raise HTTPException(
                status_code=404, detail='Organization not updated')

    return router
