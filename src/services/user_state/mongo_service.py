from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from config import MONGO_URI, MONGO_DB, MONGO_USER_STATE_COLLECTION
from models.user_state import UserState


class UserStateMongoService:
    """
    Service class to interact with MongoDB for managing user states.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB client and selects the appropriate database and collection.
        """
        self.mongo_client: MongoClient = MongoClient(MONGO_URI)
        self.db: Database = self.mongo_client[MONGO_DB]
        self.user_state_collection: Collection = self.db[MONGO_USER_STATE_COLLECTION]

    def save_user_state(self, user_state: UserState) -> None:
        """
        Saves or updates a user's state in the MongoDB collection.

        Args:
            user_state (UserState): The user state to save or update.
        """
        self.user_state_collection.update_one(
            {'user_id': user_state.user_id},
            {'$set': user_state.model_dump()},
            upsert=True
        )

    def get_user_state(self, user_id: str) -> Optional[UserState]:
        """
        Retrieves a user's state from the MongoDB collection.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[UserState]: The retrieved user state, or None if not found.
        """
        user_data = self.user_state_collection.find_one({'user_id': user_id})
        if user_data:
            return UserState(**user_data)

    def delete_user_state(self, user_id: str) -> None:
        """
        Deletes a user's state from the MongoDB collection.

        Args:
            user_id (str): The unique identifier of the user.
        """
        self.user_state_collection.delete_one({'user_id': user_id})
