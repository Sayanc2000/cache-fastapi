from typing import List

from fastapi import Request
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, Response

from cache_fastapi.wrappers import retrieve_cache, create_cache


class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            cached_endpoints: List[str],
    ):
        super().__init__(app)
        self.cached_endpoints = cached_endpoints

    def matches_any_path(self, path_url):
        for pattern in self.cached_endpoints:
            if pattern in path_url:
                return True
        return False

    async def dispatch(self, request: Request, call_next) -> Response:
        path_url = request.url.path
        request_type = request.method
        cache_control = request.headers.get('Cache-Control', None)
        auth = request.headers.get('Authorization', "token public")
        token = auth.split(" ")[1]

        key = f"{path_url}_{token}"

        matches = self.matches_any_path(path_url)

        if not matches or request_type != 'GET':
            return await call_next(request)

        stored_cache = await retrieve_cache(key)

        res = stored_cache and cache_control != 'no-cache'

        if not res:
            response: Response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))

            if response.status_code == 200:
                if cache_control == 'no-store':
                    return response

                if not cache_control:
                    max_age = 60
                elif "max-age" in cache_control:
                    max_age = int(cache_control.split("=")[1])
                else:
                    max_age = 60
                await create_cache(response_body[0].decode(), key, max_age)
            return response

        else:
            # If the response is cached, return it directly
            json_data_str = stored_cache[0].decode('utf-8')
            headers = {
                'Cache-Control': f"max-age:{stored_cache[1]}"
            }
            return StreamingResponse(iter([json_data_str]), media_type="application/json", headers=headers)
