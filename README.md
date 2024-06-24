# Cache-FastAPI

[![Python](https://shields.io/pypi/pyversions/cache_fastapi)](https://badge.fury.io/py/fastapi)
[![PyPI version](https://badge.fury.io/py/cache-fastapi.svg)](https://badge.fury.io/py/cache_fastapi)

| **Documentation**                                                                                                                           |
|---------------------------------------------------------------------------------------------------------------------------------------------|
| [![Documentation](https://img.shields.io/badge/docs-passing-brightgree)](https://github.com/Sayanc2000/cache-fastapi/blob/master/README.md) |

A lightweight caching library which leverages FastAPI's middleware functionality
and follows best practices of cache-control to easily speed up your large requests.

## How to Use
1. The packages can be included in your project by running </br>
    `pip install cache-fastapi` OR `poetry add cache-fastapi`
2. To get started you need to import the cache-fastapi middleware and then add it to your FastAPI app </br>
    ```
    from fastapi import FastAPI
    from cache_fastapi.cacheMiddleware import CacheMiddleware
    from cache_fastapi.Backends.memory_backend import MemoryBackend

    cached_endpoints = [
        "/test"
    ]

    app = FastAPI()
    backend = MemoryBackend()
    app.add_middleware(CacheMiddleware, cached_endpoints=cached_endpoints, backend=backend)
   ```
    For nested routes just add the base route:
    For example if you have routes `/data/{data_id}`, you can just add `/data/` to the `cached_endpoints`list
    ```
   cached_endpoints = [
        "/test",
        "/data/"
    ]
   ```

3. The cached_endpoints can be used to define all the endpoints you want to cache. 
    This gives you can central place where you can keep track of all the cached endpoints.
4. The default cache max-age is 60 secs, to overwrite that in the API request send the following header
    </br>`Cache-Control: max-age=time`
    </br>Here time needs to be in seconds.
5. Once a response is cached, you'll be able to get the cached response age in the response header `Cache-Control`
6. To overwrite the cache and get a fresh response use </br>
    `Cache-Control: no-cache`
7. If you want to make a request and do not want that request to be considered for caching you can use </br>
    `Cache-Control: no-store`


## Backend
The library supports multiple backends for various use cases:
1. **MemoryBackend**: This backend stores the responses in memory of the server run program. This is useful for development purposes, or when you do want to handle extra caching infra.
    It should be used for caches which are not required to be persistent.
2. **RedisBackend**: This backend stores the responses in a Redis server. This is useful for production purposes.
    It comes with the additional responsibility of handling your self-hosted redis server. </br> 
    To use the RedisBackend, you need to set the `REDIS_URL` environment variable.
