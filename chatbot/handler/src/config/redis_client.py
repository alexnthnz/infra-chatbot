from datetime import datetime

import redis
from .config import config


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            decode_responses=True
        )

    def blacklist_token(self, token: str, expires_at: datetime):
        # Calculate remaining TTL in seconds
        ttl = int((expires_at - datetime.utcnow()).total_seconds())
        if ttl > 0:
            self.client.setex(token, ttl, "blacklisted")

    def is_token_blacklisted(self, token: str) -> bool:
        return self.client.exists(token) == 1


redis_client = RedisClient()
