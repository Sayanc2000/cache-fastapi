import time

from fastapi import FastAPI
from pydantic import BaseModel

from cache_fastapi.Backends.memory_backend import MemoryBackend
from cache_fastapi.cacheMiddleware import CacheMiddleware

cached_endpoints = [
    "/test",
    "/data/update"
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


class Data(BaseModel):
    x: int
    y: int


@app.post("/data/update")
def update_data(data: Data):
    print("Endpoint invoked ", data)
    for i in range(2):
        time.sleep(0.5)
    return {
        "resp": "updated"
    }
