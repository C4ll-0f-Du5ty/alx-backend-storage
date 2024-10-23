#!/usr/bin/env python3
"""_summary_

    Returns:
        _type_: _description_
    """

import redis
import uuid
import typing

class Cache():
    """_summary_

    Returns:
        _type_: _description_
    """

    def __init__(self):
        self._redis: redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: typing.Union[str, bytes, int, float]) -> str:
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
