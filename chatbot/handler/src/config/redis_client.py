import redis
import json
from datetime import datetime
from .config import config


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            decode_responses=True,
        )

    def store_user_info(self, user_id: str, user_info: dict, ttl_seconds: int = 86400):
        """
        Store user information in Redis as JSON with a TTL.

        Args:
            user_id (str): User ID to use as part of the key (format: user:<user_id>).
            user_info (dict): User data to store (e.g., email, username).
            ttl_seconds (int): Time to live in seconds (default: 1 day = 86400).
        """
        key = f"user:{user_id}"
        self.client.setex(key, ttl_seconds, json.dumps(user_info))

    def get_user_info(self, user_id: str) -> dict | None:
        """
        Retrieve user information from Redis.

        Args:
            user_id (str): User ID to retrieve the info for.

        Returns:
            dict | None: User data as a dict if found, None otherwise.
        """
        key = f"user:{user_id}"
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def delete_user_info(self, user_id: str):
        """
        Delete user information from Redis.

        Args:
            user_id (str): User ID to delete the info for.
        """
        key = f"user:{user_id}"
        self.client.delete(key)

    def store_access_token_jti(self, user_id: str, jti: str, ttl_seconds: int = 86400):
        """
        Store the jti of an access token in Redis with a TTL.

        Args:
            user_id (str): User ID to use as part of the key (format: token:jti:<user_id>).
            jti (str): Unique token identifier.
            ttl_seconds (int): Time to live in seconds (default: 1 day = 86400).
        """
        key = f"token:jti:{user_id}"
        self.client.setex(key, ttl_seconds, jti)

    def get_access_token_jti(self, user_id: str) -> str | None:
        """
        Retrieve the jti of an access token from Redis.

        Args:
            user_id (str): User ID to retrieve the jti for.

        Returns:
            str | None: Stored jti if found, None otherwise.
        """
        key = f"token:jti:{user_id}"
        return self.client.get(key)

    def delete_access_token_jti(self, user_id: str):
        """
        Delete the jti of an access token from Redis.

        Args:
            user_id (str): User ID to delete the jti for.
        """
        key = f"token:jti:{user_id}"
        self.client.delete(key)

    def blacklist_token(self, token: str, expires_at: datetime):
        """
        Blacklist a refresh token with a TTL based on expiration.

        Args:
            token (str): Refresh token to blacklist.
            expires_at (datetime): Token expiration time.
        """
        ttl = int((expires_at - datetime.utcnow()).total_seconds())
        if ttl > 0:
            self.client.setex(f"blacklist:{token}", ttl, "blacklisted")

    def is_token_blacklisted(self, token: str) -> bool:
        """
        Check if a refresh token is blacklisted.

        Args:
            token (str): Refresh token to check.

        Returns:
            bool: True if blacklisted, False otherwise.
        """
        return self.client.exists(f"blacklist:{token}") == 1


redis_client = RedisClient()
