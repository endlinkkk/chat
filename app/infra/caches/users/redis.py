from abc import ABC
from dataclasses import dataclass

from infra.caches.users.base import BaseUserCache

from redis.asyncio import Redis

from settings.config import CacheConfig


@dataclass
class BaseRedisUserCache(ABC):
    redis_client: Redis

    @property
    def _cache(self):
        return self.redis_client


@dataclass
class RedisUserCache(BaseRedisUserCache, BaseUserCache):
    cache_config: CacheConfig

    async def add_code(self, phone: str, code: str):
        ex = self.cache_config.cache_expire_seconds
        await self._cache.set(phone, code, ex=ex)

    async def delete_code(self, phone: str):
        await self._cache.delete(phone)

    async def check_code(self, phone: str, code: str) -> bool:
        saved_code: bytes | None = await self._cache.get(phone)
        if saved_code:
            saved_code = saved_code.decode()
        return saved_code == code if saved_code is not None else False
