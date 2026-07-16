import redis.asyncio as aioredis

from core.config import config

redis = aioredis.from_url(url=config.REDIS_URI)
