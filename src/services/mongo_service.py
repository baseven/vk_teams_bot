from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION
from models.user_state import UserState
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient as MongoClientType
from typing import Optional


class MongoService:
    def __init__(self) -> None:
        self.mongo_client: MongoClientType = MongoClient(MONGO_URI)
        self.db: Database = self.mongo_client[MONGO_DB]
        self.users_collection: Collection = self.db[MONGO_COLLECTION]

    def save_state(self, user_state: UserState) -> None:
        self.users_collection.update_one(
            {'user_id': user_state.user_id},
            {'$set': {'state': user_state.state,
                      'last_message_id': user_state.last_message_id,
                      'start_date': user_state.start_date,
                      'end_date': user_state.end_date}},
            upsert=True
        )

    def load_state(self, user_id: str) -> Optional[UserState]:
        user_data: Optional[dict] = self.users_collection.find_one({'user_id': user_id})
        if user_data:
            state = user_data.get('state', 'main_menu')
            last_message_id = user_data.get('last_message_id')
            start_date = user_data.get('start_date')
            end_date = user_data.get('end_date')
            return UserState(user_id=user_id, state=state, last_message_id=last_message_id, start_date=start_date,
                             end_date=end_date)
