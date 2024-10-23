#!/usr/bin/env python3

import redis
import uuid
class Cache():

    def __init__(self):
        _redis = redis.Redis()
        _redis.flushdb()

    def store(self, data) -> str:
        key = uuid.uuid4()
        self._redis.set(key, data)
        return key
