from typing import Optional

from models.user_state import UserState
from services.user_state import UserStateMongoService, UserStateRedisService


class UserStateDatabaseService:
    """
    Service class to manage user states across MongoDB and Redis.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB and Redis services.
        """
        self.mongo_service: UserStateMongoService = UserStateMongoService()
        self.redis_service: UserStateRedisService = UserStateRedisService()

    def save_user_state(self, user_state: UserState) -> None:
        """
        Saves or updates a user's state in both Redis (for quick access) and MongoDB (for long-term storage).

        Args:
            user_state (UserState): The user state to save or update.
        """
        self.redis_service.save_user_state(user_state)
        self.mongo_service.save_user_state(user_state)

    def get_user_state(self, user_id: str) -> Optional[UserState]:
        """
        Retrieves a user's state from Redis or MongoDB.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[UserState]: The retrieved user state, or None if not found.
        """
        user_state = self.redis_service.get_user_state(user_id)
        if user_state:
            return user_state

        user_state = self.mongo_service.get_user_state(user_id)
        if user_state:
            # Cache the retrieved state back in Redis for future quick access
            self.redis_service.save_user_state(user_state)
            return user_state

    def delete_user_state(self, user_id: str) -> None:
        """
        Deletes a user's state from both Redis and MongoDB.

        Args:
            user_id (str): The unique identifier of the user.
        """
        self.redis_service.delete_user_state(user_id)
        self.mongo_service.delete_user_state(user_id)
