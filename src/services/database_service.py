from services.mongo_service import MongoService
from services.redis_service import RedisService
from models.user_state import UserState
from typing import Optional


class DatabaseService:
    def __init__(self) -> None:
        self.mongo_service: MongoService = MongoService()
        self.redis_service: RedisService = RedisService()

    def save_state(self, user_state: UserState) -> None:
        self.redis_service.save_state(user_state)
        self.mongo_service.save_state(user_state)

    def load_state(self, user_id: str) -> UserState:
        user_state: Optional[UserState] = self.redis_service.load_state(user_id)
        if user_state:
            return user_state
        user_state = self.mongo_service.load_state(user_id)
        if user_state:
            return user_state
        user_state = UserState(user_id=user_id, state='main_menu')
        self.save_state(user_state)
        return user_state
