import redis.asyncio as redis

from ..config import settings


class RedisState:
    def __init__(self):
        self.pool = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)
        self.client = redis.Redis(connection_pool=self.pool)

    async def get(self, key: str):
        return await self.client.get(key)

    async def set(self, key: str, value: str, ex: int | None = None):
        await self.client.set(key, value, ex=ex)

    async def keys(self, pattern: str):
        return await self.client.keys(pattern)

    async def close(self):
        await self.client.close()
        await self.pool.disconnect()


redis_state = RedisState()
