import time
from fastapi import FastAPI

from caching.cacheMiddleware import CacheMiddleware

cached_endpoints = [
    "/test"
]

app = FastAPI()
app.add_middleware(CacheMiddleware, cached_endpoints=cached_endpoints)


@app.get("/test")
def root():
    for i in range(2):
        time.sleep(0.5)
    return {
        "hello": "world"
    }
