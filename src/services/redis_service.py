from typing import Optional

import redis
from redis.client import StrictRedis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from models.user_data import UserData


class UserDataRedisService:
    """
    Service class to interact with Redis for managing user data.
    """

    def __init__(self) -> None:
        """
        Initializes the Redis client with the specified configuration.
        """
        self.redis_client: StrictRedis = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB
        )

    def save_user_data(self, user_data: UserData) -> None:
        """
        Saves or updates a user's data in the Redis store.

        Args:
            user_data (UserData): The user data to save or update.
        """
        self.redis_client.hset(user_data.user_id, mapping=user_data.model_dump())

    def get_user_data(self, user_id: str) -> Optional[UserData]:
        """
        Retrieves a user's data from the Redis store.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[UserData]: The retrieved user data, or None if not found.
        """
        data = self.redis_client.hgetall(user_id)
        if data:
            return UserData(**{key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()})

    def delete_user_data(self, user_id: str) -> None:
        """
        Deletes a user's data from the Redis store.

        Args:
            user_id (str): The unique identifier of the user.
        """
        self.redis_client.delete(user_id)
