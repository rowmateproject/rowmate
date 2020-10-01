from bson.binary import Binary, UUID_SUBTYPE
from uuid import uuid4


def generate_uuid() -> Binary:
    return Binary(bytes(bytearray(uuid4().bytes)), UUID_SUBTYPE)
