import redis
from redis.client import StrictRedis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from models.user_state import UserState
from typing import Optional, Union


class RedisService:
    def __init__(self) -> None:
        self.redis_client: StrictRedis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def save_state(self, user_state: UserState) -> None:
        self.redis_client.set(name=user_state.user_id, value=user_state.state)

    def load_state(self, user_id: str) -> Optional[UserState]:
        state: Union[bytes, None] = self.redis_client.get(user_id)
        if state:
            return UserState(user_id=user_id, state=state.decode('utf-8'))
