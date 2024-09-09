from typing import Optional

import redis
from redis.client import StrictRedis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from models.user_state import UserState


class UserStateRedisService:
    """
    Service class to interact with Redis for managing user states.
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

    def save_user_state(self, user_state: UserState) -> None:
        """
        Saves or updates a user's state in the Redis store.

        Args:
            user_state (UserState): The user state to save or update.
        """
        self.redis_client.hset(user_state.user_id, mapping=user_state.model_dump())

    def get_user_state(self, user_id: str) -> Optional[UserState]:
        """
        Retrieves a user's state from the Redis store.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[UserState]: The retrieved user state, or None if not found.
        """
        data = self.redis_client.hgetall(user_id)
        if data:
            return UserState(**{key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()})

    def delete_user_state(self, user_id: str) -> None:
        """
        Deletes a user's state from the Redis store.

        Args:
            user_id (str): The unique identifier of the user.
        """
        self.redis_client.delete(user_id)
