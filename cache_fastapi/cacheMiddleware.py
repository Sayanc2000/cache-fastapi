import hashlib
import json
import logging
from typing import List

from fastapi import Request
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, Response

from cache_fastapi.Backends.base_backend import BaseBackend

logger = logging.getLogger(__name__)


class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            cached_endpoints: List[str],
            backend: BaseBackend
    ):
        super().__init__(app)
        self.cached_endpoints = cached_endpoints
        self.backend = backend

    def matches_any_path(self, path_url):
        for pattern in self.cached_endpoints:
            if pattern in path_url:
                return True
        return False

    def generate_body_hash(self, body: str) -> str:
        """
        Generate a fixed-length hash for the request body.

        Args:
            body (str): The request body to hash

        Returns:
            str: A fixed-length SHA-256 hash of the body
        """
        # Use SHA-256 to create a consistent hash
        return hashlib.sha256(body.encode('utf-8')).hexdigest()

    async def get_request_body(self, request: Request) -> str:
        """
        Safely retrieve the request body for caching.
        Works for both GET and POST requests.
        Always returns a string can be empty
        """
        body_str = ""
        try:
            # For POST requests, read the body
            if request.method == 'POST':
                body_bytes = await request.body()
                # Try to decode and parse JSON if possible
                try:
                    body_dict = await request.json()
                    # Sort the dictionary to ensure consistent key ordering
                    body_str = json.dumps(body_dict, sort_keys=True)
                except:
                    # If not JSON, use the raw bytes
                    body_str = body_bytes.decode('utf-8')
            return body_str
        except Exception as e:
            logger.warning("Error reading request body: ", e)
            return body_str

    async def dispatch(self, request: Request, call_next) -> Response:
        path_url = request.url.path
        request_type = request.method
        cache_control = request.headers.get('Cache-Control', 'max-age=60')
        auth = request.headers.get('Authorization', "token public")
        token = auth.split(" ")[1]

        # Get request body for POST requests
        request_body = await self.get_request_body(request)

        # Generate a fixed-length hash for the body
        body_hash = self.generate_body_hash(request_body)

        # Create a cache key that includes path, token, and hashed body
        key = f"{path_url}_{token}_{body_hash}"

        matches = self.matches_any_path(path_url)

        # Only cache GET and POST requests
        if not matches or (request_type not in ['GET', 'POST']) or cache_control == 'no-cache':
            return await call_next(request)

        # Check if response is cached
        res = await self.backend.retrieve(key)
        if not res:
            # If not cached, proceed with the request
            response: Response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))

            if response.status_code == 200:
                # Skip caching for no-store
                if cache_control == 'no-store':
                    return response

                # Determine max-age
                if not cache_control:
                    max_age = 60
                elif "max-age" in cache_control:
                    max_age = int(cache_control.split("=")[1])
                else:
                    max_age = 60

                # Cache the response
                await self.backend.create(response_body[0].decode(), key, max_age)

            return response
        else:
            # If the response is cached, return it directly
            json_data_str = res[0].decode('utf-8')
            headers = {
                'Cache-Control': f"max-age:{res[1]}"
            }
            return StreamingResponse(iter([json_data_str]), media_type="application/json", headers=headers)
