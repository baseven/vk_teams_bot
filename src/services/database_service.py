from typing import Optional

from models.user_data import UserData
from services.user_state import UserDataMongoService, UserDataRedisService


class UserDataDatabaseService:
    """
    Service class to manage user data across MongoDB and Redis.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB and Redis services.
        """
        self.mongo_service: UserDataMongoService = UserDataMongoService()
        self.redis_service: UserDataRedisService = UserDataRedisService()

    def save_user_data(self, user_data: UserData) -> None:
        """
        Saves or updates a user's data in both Redis (for quick access) and MongoDB (for long-term storage).

        Args:
            user_data (UserData): The user data to save or update.
        """
        self.redis_service.save_user_data(user_data)
        self.mongo_service.save_user_data(user_data)

    def get_user_data(self, user_id: str) -> Optional[UserData]:
        """
        Retrieves a user's data from Redis or MongoDB.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[UserData]: The retrieved user data, or None if not found.
        """
        user_data = self.redis_service.get_user_data(user_id)
        if user_data:
            return user_data

        user_data = self.mongo_service.get_user_data(user_id)
        if user_data:
            # Cache the retrieved data back in Redis for future quick access
            self.redis_service.save_user_data(user_data)
            return user_data

    def delete_user_data(self, user_id: str) -> None:
        """
        Deletes a user's data from both Redis and MongoDB.

        Args:
            user_id (str): The unique identifier of the user.
        """
        self.redis_service.delete_user_data(user_id)
        self.mongo_service.delete_user_data(user_id)
