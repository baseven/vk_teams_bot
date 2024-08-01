from pydantic import BaseModel
from typing import Optional


class UserState(BaseModel):
    user_id: str
    state: str
    last_message_id: Optional[str] = None
