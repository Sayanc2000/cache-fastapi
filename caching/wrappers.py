from redis import asyncio as aioredis

redis = aioredis.from_url('redis://redis:6379')


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
