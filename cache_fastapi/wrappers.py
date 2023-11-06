from redis import asyncio as aioredis
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_URL = os.environ.get('REDIS_URL', None)
if not REDIS_URL:
    raise Exception("Please add REDIS_URL in environment")

redis = aioredis.from_url(REDIS_URL)


async def create_cache(resp, key: str, ex: int = 60):
    await redis.set(key, resp, ex=ex)


async def retrieve_cache(key: str):
    data = await redis.get(key)
    if not data:
        return None
    expire = await redis.ttl(key)
    return data, expire


async def invalidate_cache(key: str):
    await redis.delete(key)
