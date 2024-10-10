from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from src.config import MONGO_URI, MONGO_DB, MONGO_USER_DATA_COLLECTION
from src.models.user_data import UserData


class UserDataMongoService:
    """
    Service class to interact with MongoDB for managing user data.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB client and selects the appropriate database and collection.
        """
        self.mongo_client: MongoClient = MongoClient(MONGO_URI)
        self.db: Database = self.mongo_client[MONGO_DB]
        self.user_data_collection: Collection = self.db[MONGO_USER_DATA_COLLECTION]

    def save_user_data(self, user_data: UserData) -> None:
        """
        Saves or updates a user's data in the MongoDB collection.

        Args:
            user_data (UserData): The user data to save or update.
        """
        self.user_data_collection.update_one(
            {'user_id': user_data.user_id},
            {'$set': user_data.model_dump()},
            upsert=True
        )

    def get_user_data(self, user_id: str) -> Optional[UserData]:
        """
        Retrieves a user's data from the MongoDB collection.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[UserData]: The retrieved user data, or None if not found.
        """
        user_data = self.user_data_collection.find_one({'user_id': user_id})
        if user_data:
            return UserData(**user_data)

    def delete_user_data(self, user_id: str) -> None:
        """
        Deletes a user's data from the MongoDB collection.

        Args:
            user_id (str): The unique identifier of the user.
        """
        self.user_data_collection.delete_one({'user_id': user_id})
