from fastapi import Response

# auth
from auth.user import Authentication

# utils
from utils.jwt import generate_jwt

import pytest
import jwt


SECRET = 'SECRET'
ACCESS_LIFETIME = 3600
REFRESH_LIFETIME = 50000


@pytest.fixture
def jwt_auth():
    return Authentication(SECRET, ACCESS_LIFETIME, REFRESH_LIFETIME)


@pytest.fixture
def token():
    def _token(user_id=None, lifetime=ACCESS_LIFETIME):
        data = {'aud': 'jwt:auth'}

        if user_id is not None:
            data['user_id'] = str(user_id)

        return generate_jwt(data, SECRET, lifetime)

    return _token


def test_default_name(jwt_auth):
    assert jwt_auth.name == 'jwt'


class TestAuthenticate:
    @pytest.mark.asyncio
    async def test_missing_token(self, jwt_auth, mock_user_db):
        authenticated_user = await jwt_auth(None, mock_user_db)
        assert authenticated_user is None

    @pytest.mark.asyncio
    async def test_invalid_token(self, jwt_auth, mock_user_db):
        authenticated_user = await jwt_auth('foo', mock_user_db)
        assert authenticated_user is None

    @pytest.mark.asyncio
    async def test_valid_token_missing_user_payload(
            self, jwt_auth, mock_user_db, token):
        authenticated_user = await jwt_auth(token(), mock_user_db)
        assert authenticated_user is None

    @pytest.mark.asyncio
    async def test_valid_token_invalid_uuid(
            self, jwt_auth, mock_user_db, token):
        authenticated_user = await jwt_auth(
            token('foo'), mock_user_db)
        assert authenticated_user is None

    @pytest.mark.asyncio
    async def test_valid_token(
            self, jwt_auth, mock_user_db, token, user):
        print(self, jwt_auth, mock_user_db, token)
        authenticated_user = await jwt_auth(
            token(user.id), mock_user_db)
        print(authenticated_user)
        assert authenticated_user.id == user.id


@pytest.mark.asyncio
async def test_get_login_response(jwt_auth, user):
    login_response = await jwt_auth.get_login_response(
        user, Response())

    assert 'access_token' in login_response
    assert login_response['token_type'] == 'bearer'

    token = login_response['access_token']
    decoded = jwt.decode(
        token, SECRET, audience='jwt:auth', algorithms=['HS256']
    )
    assert decoded['user_id'] == str(user.id)


@pytest.mark.asyncio
async def test_get_logout_response(jwt_auth, user):
    with pytest.raises(NotImplementedError):
        await jwt_auth.get_logout_response(user, Response())
