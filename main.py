import time
from starlette.concurrency import iterate_in_threadpool

from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse

from caching.wrappers import retrieve_cache, create_cache

app = FastAPI()

cached_endpoints = [
    "/test"
]


@app.middleware("http")
async def cache_check_header(request: Request, call_next):
    path_url = request.url.path
    cache_control = request.headers.get('Cache-Control', None)

    if path_url not in cached_endpoints:
        return await call_next(request)

    stored_cache = await retrieve_cache(path_url)

    res = stored_cache and cache_control != 'no-cache'

    if not res:
        response: StreamingResponse = await call_next(request)
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        await create_cache(response_body[0].decode(), path_url)

        return response

    else:
        # If the response is cached, return it directly
        json_data_str = stored_cache.decode('utf-8')
        return StreamingResponse(iter([json_data_str]), media_type="application/json")


@app.get("/test")
def root():
    for i in range(2):
        time.sleep(0.5)
    return {
        "hello": "world"
    }
