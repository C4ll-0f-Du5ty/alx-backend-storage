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


    def get(self, key: str, fn: typing.Optional[callable] = None) -> typing.Union[str, bytes, int, float]:
        """_summary_

        Args:
            key (str): _description_
            fn (typing.Optional[callable], optional): _description_. Defaults to None.

        Returns:
            typing.Union[str, bytes, int, float]: _description_
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value


    def get_str(self, key: str) -> str:
        """automatically parametrize Cache.get with the correct
        conversion function"""
        value = self._redis.get(key)
        return value.decode("utf-8")


    def get_int(self, key: str) -> int:
        """automatically parametrize Cache.get with the correct
        conversion function"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
