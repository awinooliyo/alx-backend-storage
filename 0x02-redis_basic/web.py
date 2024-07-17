#!/usr/bin/env python3
"""Expiring web cache module"""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """Decorator to wrap requests and cache results"""

    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper function to count and cache requests"""
        redis_client.incr(f"count:{url}")
        cached_response = redis_client.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        result = fn(url)
        redis_client.setex(f"cached:{url}", 10, result)
        return result

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """Get the HTML content of a URL and cache it"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = ("http://slowwly.robertomurray.co.uk/delay/5000/url/"
           "http://www.google.com")
    print(get_page(url))
    print(get_page(url))
