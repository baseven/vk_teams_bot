import logging
from typing import Optional

import redis
from redis.client import StrictRedis

from src.config import REDIS_HOST, REDIS_PORT, REDIS_DB
from src.models.user_data import UserData

logger = logging.getLogger(__name__)


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
        user_data_json = user_data.model_dump_json(exclude_none=True)
        self.redis_client.set(user_data.user_id, user_data_json)

    def get_user_data(self, user_id: str) -> Optional[UserData]:
        """
        Retrieves a user's data from the Redis store.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[UserData]: The retrieved user data, or None if not found.
        """
        raw_user_data = self.redis_client.get(user_id)
        if raw_user_data:
            # If you are using the option decode_responses=True when creating the Redis client,
            # Redis will automatically return strings instead of bytes, and no decoding will be required.
            user_data_json = raw_user_data.decode('utf-8') if isinstance(raw_user_data, bytes) else raw_user_data
            return UserData.model_validate_json(user_data_json)

    def delete_user_data(self, user_id: str) -> None:
        """
        Deletes a user's data from the Redis store.

        Args:
            user_id (str): The unique identifier of the user.
        """
        self.redis_client.delete(user_id)
