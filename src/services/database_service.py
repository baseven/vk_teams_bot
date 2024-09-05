from typing import Optional

from services.mongo_service import MongoService
from services.redis_service import RedisService
from models.user_state import UserState


class DatabaseService:
    """
    Service class to manage user states across MongoDB and Redis.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB and Redis services.
        """
        self.mongo_service: MongoService = MongoService()
        self.redis_service: RedisService = RedisService()

    def save_state(self, user_state: UserState) -> None:
        """
        Saves or updates a user's state in both Redis and MongoDB.

        Args:
            user_state (UserState): The user state to save or update.
        """
        # Save to Redis for quick access
        self.redis_service.save_state(user_state)
        # Also save to MongoDB for long-term storage
        self.mongo_service.save_state(user_state)

    def get_user_state(self, user_id: str) -> Optional[UserState]:
        """
        Retrieves a user's state from Redis or MongoDB.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[UserState]: The retrieved user state, or None if not found.
        """
        user_state = self.redis_service.get_state(user_id)
        if user_state:
            return user_state

        user_state = self.mongo_service.get_state(user_id)
        if user_state:
            # Cache the retrieved state back in Redis for future quick access
            self.redis_service.save_state(user_state)
            return user_state

    def delete_user_state(self, user_id: str) -> None:
        """
        Deletes a user's state from both Redis and MongoDB.

        Args:
            user_id (str): The unique identifier of the user.
        """
        # Remove user state from both Redis and MongoDB
        self.redis_service.delete_state(user_id)
        self.mongo_service.delete_state(user_id)
