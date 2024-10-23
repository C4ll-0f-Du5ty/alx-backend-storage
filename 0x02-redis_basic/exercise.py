#!/usr/bin/env python3
"""_summary_

    Returns:
        _type_: _description_
    """

import redis
import uuid
import typing
import functools

def count_calls(method: typing.Callable) -> typing.Callable:
    """returns a Callable"""
    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorated function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: typing.Callable) -> typing.Callable:
    """store the history of inputs and outputs"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the decorated function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(fn: typing.Callable):
    """display the history of calls of a particular function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    # print(f"{function_name} was called {value} times")
    print("{} was called {} times:".format(function_name, value))
    # inputs = r.lrange(f"{function_name}:inputs", 0, -1)
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    # outputs = r.lrange(f"{function_name}:outputs", 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        # print(f"{function_name}(*{input}) -> {output}")
        print("{}(*{}) -> {}".format(function_name, input, output))


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
