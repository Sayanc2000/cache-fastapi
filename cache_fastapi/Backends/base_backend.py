from typing import Any


class BaseBackend:
    def __init__(self):
        self.cache = {}

    def create(self, resp, key: str, ex: int = 60):
        raise NotImplementedError

    def retrieve(self, key: str):
        raise NotImplementedError

    def invalidate(self, key: str):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError
