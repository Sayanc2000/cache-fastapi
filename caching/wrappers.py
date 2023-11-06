from redis import asyncio as aioredis

redis = aioredis.from_url('redis://redis:6379')


async def create_cache(resp, key):
    await redis.set(key, resp, ex=60)


async def retrieve_cache(key):
    return await redis.get(key)


async def invalidate_cache(key):
    await redis.delete(key)