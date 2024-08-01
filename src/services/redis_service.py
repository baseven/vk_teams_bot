import redis
from redis.client import StrictRedis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from models.user_state import UserState
from typing import Optional, Union

class RedisService:
    def __init__(self) -> None:
        self.redis_client: StrictRedis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def save_state(self, user_state: UserState) -> None:
        # Использование hset для установки значений в хэш
        self.redis_client.hset(user_state.user_id, mapping={
            "state": user_state.state or 'main_menu',
            "last_message_id": user_state.last_message_id or ''
        })

    def load_state(self, user_id: str) -> Optional[UserState]:
        data = self.redis_client.hgetall(user_id)
        if data:
            state = data.get(b'state', b'main_menu').decode('utf-8')
            last_message_id = data.get(b'last_message_id', b'').decode('utf-8')
            return UserState(user_id=user_id, state=state, last_message_id=last_message_id)
