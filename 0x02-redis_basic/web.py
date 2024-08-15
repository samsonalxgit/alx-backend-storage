#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import requests
from cachetools import TTLCache, cached
from cachetools.keys import hashkey

# Create a cache with a time-to-live (TTL) of 10 seconds
cache = TTLCache(maxsize=100, ttl=10)
url_access_count = {}

def cache_decorator(func):
    def wrapper(url: str) -> str:
        # Increment the access count for the URL
        if url in url_access_count:
            url_access_count[url] += 1
        else:
            url_access_count[url] = 1

        # Check the cache first
        if url in cache:
            return cache[url]

        # Call the original function and cache the result
        result = func(url)
        cache[url] = result
        return result
    return wrapper

@cache_decorator
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Test the function
    test_url = "http://slowwly.robertomurray.co.uk/"
    print(get_page(test_url))

