#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate
a slow response and test your caching."""


import requests
import redis
from functools import wraps

store = redis.Redis()

def count_url_access(method):
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        count = store.get(count_key)
        if count is None:
            store.set(count_key, 1, ex=10)  # Initialize count to 1 and set a 10-second expiration

        html = method(url)

        store.incr(count_key)  # Increment the access count
        store.set(cached_key, html)
        store.expire(cached_key, 10)

        return html

    return wrapper

@count_url_access
def get_page(url: str) -> str:
    res = requests.get(url)
    return res.text

