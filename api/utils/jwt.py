from datetime import datetime, timedelta

import jwt


def generate_jwt(data: dict, secret: str, lifetime_seconds: int) -> str:
    expires = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
    data['exp'] = expires

    return jwt.encode(data, secret, algorithm='HS256')
