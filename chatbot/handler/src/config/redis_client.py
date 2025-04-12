from datetime import datetime
import json
import redis
from .config import config


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            decode_responses=True,
        )

    def blacklist_token(self, token: str, expires_at: datetime):
        # Calculate remaining TTL in seconds
        ttl = int((expires_at - datetime.utcnow()).total_seconds())
        if ttl > 0:
            self.client.setex(token, ttl, "blacklisted")

    def is_token_blacklisted(self, token: str) -> bool:
        return self.client.exists(token) == 1

    def store_user_data(self, user_id: str, user_data: dict, ttl_seconds: int = 3600):
        """
        Store user data in Redis with TTL

        Args:
            user_id: User ID to use as key
            user_data: User data to store
            ttl_seconds: Time to live in seconds (default: 1 hour)
        """
        key = f"user:{user_id}"
        self.client.setex(key, ttl_seconds, json.dumps(user_data))

    def get_user_data(self, user_id: str) -> dict:
        """
        Get user data from Redis

        Args:
            user_id: User ID to retrieve

        Returns:
            dict: User data or None if not found
        """
        key = f"user:{user_id}"
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def delete_user_data(self, user_id: str):
        """
        Delete user data from Redis

        Args:
            user_id: User ID to delete
        """
        key = f"user:{user_id}"
        self.client.delete(key)


redis_client = RedisClient()
