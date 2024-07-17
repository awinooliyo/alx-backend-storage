#!/usr/bin/env python3
"""
Redis module
"""
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Count how many times methods of the Cache class are called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrap the method to count calls.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Store the history of inputs and outputs for a particular function.
    """
    key = method.__qualname__
    i = f"{key}:inputs"
    o = f"{key}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrap the method to store call history."""
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


class Cache:
    """
    Cache redis class
    """

    def __init__(self):
        """
        Constructor of the Cache class.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Generate a random key and store data in Redis using the random key.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> UnionOfTypes:
        """
        Retrieve data from Redis and optionally convert it using fn.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_int(self: bytes) -> int:
        """Convert bytes to an integer."""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """Convert bytes to a string."""
        return self.decode("utf-8")


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    """
    redis_instance = method.__self__._redis
    method_qualname = method.__qualname__

    input_key = f"{method_qualname}:inputs"
    output_key = f"{method_qualname}:outputs"

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    print(f"{method_qualname} was called {len(inputs)} times:")

    for input_str, output_str in zip(inputs, outputs):
        input_args = input_str.decode('utf-8')
        output_val = output_str.decode('utf-8')
        print(f"{method_qualname}(*{input_args}) -> {output_val}")

