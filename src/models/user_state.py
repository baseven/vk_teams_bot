from pydantic import BaseModel


class UserState(BaseModel):
    user_id: str
    state: str
