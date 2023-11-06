# Cache-FastAPI

A lightweight caching library which leverages FastAPI's middleware functionality
and follows best practices of cache-control to easily speed up your large requests.

## How to Use
1. The packages can be included in your project by running </br>
    `pip install cache-fastapi`
2. To get started you need to import the cache-fastapi middleware and then add it to your FastAPI app </br>
    ```
    from fastapi import FastAPI
    from cache_fastapi.cacheMiddleware import CacheMiddleware

    cached_endpoints = [
        "/test"
    ]

    app = FastAPI()
    app.add_middleware(CacheMiddleware, cached_endpoints=cached_endpoints)
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

