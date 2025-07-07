from src.core.utils import Singleton
import redis
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
            self.redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
            )
            logger.info(f"Redis connect success!")
            return True
        except Exception:
            logger.error(f"Redis connect error!")
            return False

    def clear(self):
        for key in self.redis.scan_iter():
            self.redis.delete(key)

    # async def get_key(self, key: str):
    #     return await self.redis.get(key)
        
    # async def set_key(self, key: str, val: str) -> bool:
    #     await self.redis.set(key, val)
        
    def keys(self):
        return self.redis.keys()
    
    def lpop(self, redis_queue):
        return self.redis.lpop(redis_queue)

    def rpush(self, redis_queue: str, val: str):
        self.redis.rpush(redis_queue, val)

    def set_key(self, key: str, val: str) -> bool:
        self.redis.set(key, val)

    def get_key(self, key: str):
        return self.redis.get(key)