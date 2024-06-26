import time
from fastapi import FastAPI

from cache_fastapi.Backends.memory_backend import MemoryBackend
from cache_fastapi.cacheMiddleware import CacheMiddleware

cached_endpoints = [
    "/test",
    "/data/"
]

app = FastAPI()
backend = MemoryBackend()
app.add_middleware(CacheMiddleware, cached_endpoints=cached_endpoints, backend=backend)


@app.get("/test")
def root():
    for i in range(2):
        time.sleep(1)
    return [
        {"hello": "world"},
        {"test": "data"}
    ]


@app.get("/data/{data_id}")
def data_by_id(data_id: int):
    for i in range(2):
        time.sleep(0.5)
    return {
        "resp": data_id
    }


@app.get("/data")
def all_data():
    for i in range(2):
        time.sleep(0.5)
    return {
        "resp": "all data"
    }
