import os
from typing import Optional

import redis
from dotenv import load_dotenv

from cache_fastapi.Backends.base_backend import BaseBackend
from redis import asyncio as aioredis


class RedisBackend(BaseBackend):
    def __init__(self):
        super().__init__()
        load_dotenv()

        REDIS_URL = os.environ.get('REDIS_URL', None)
        self.cache = aioredis.from_url(REDIS_URL)

    async def create(self, resp, key: str, ex: int = 60):
        await self.cache.set(key, resp, ex=ex)

    async def retrieve(self, key: str):
        data = await self.cache.get(key)
        if not data:
            return None
        expire = await self.cache.ttl(key)
        return data, expire

    async def invalidate(self, key: str):
        await self.cache.delete(key)

    async def clear(self):
        await self.cache.flushdb()
