import time
from typing import Optional

from cache_fastapi.Backends.base_backend import BaseBackend


class MemoryBackend(BaseBackend):
    def __init__(self):
        super().__init__()
        self.cache = {}

    async def create(self, resp, key: str, ex: int = 60):
        self.cache[key] = {
            "data": resp,
            "expire": time.time() + ex if ex else time.time() + 9_99_99_999
        }

    async def retrieve(self, key: str):
        data = self.cache.get(key)
        if data:
            expire = data.get('expire')
            if expire:
                if expire >= time.time():
                    return data.get('data').encode('utf-8'), expire - time.time()

    def invalidate(self, key: str):
        self.cache.pop(key, None)

    def clear(self):
        self.cache.clear()
