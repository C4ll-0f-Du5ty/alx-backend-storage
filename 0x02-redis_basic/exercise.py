#!/usr/bin/env python3
"""_summary_

    Returns:
        _type_: _description_
    """

import redis
import uuid


class Cache():
    """_summary_

    Returns:
        _type_: _description_
    """
    _redis = redis.Redis()

    def __init__(self):
        Cache._redis.flushdb()

    def store(self, data) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
