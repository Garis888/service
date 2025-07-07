from src.core.utils import Singleton
import redis.asyncio
from src.config import settings
from loguru import logger


class Redis(metaclass=Singleton):
    def __init__(self):
        logger.info(f"REDIS_HOST: {settings.REDIS_HOST} REDIS_PORT: {settings.REDIS_PORT}")
        self.redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
        # self.redis_url = f"redis://localhost:6379"
        self.redis = None
        
    def init(self) -> bool:
        try:
            self.redis = redis.asyncio.from_url(
                self.redis_url,
                decode_responses=True,
            )
            logger.info(f"Redis connect success!")
            return True
        except Exception:
            logger.error(f"Redis connect error!")
            return False

    async def clear(self):
        async for key in self.redis.scan_iter():
            await self.redis.delete(key)

    async def get_key(self, key: str):
        return await self.redis.get(key)
        
    async def set_key(self, key: str, val: str) -> bool:
        await self.redis.set(key, val)
        
    async def keys(self):
        return await self.redis.keys()

    async def lpop(self, redis_queue: str):
        await self.redis.lpop(redis_queue)
    
    async def rpush(self, redis_queue: str, val: str):
        await self.redis.rpush(redis_queue, val)
