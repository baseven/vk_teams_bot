from datetime import datetime
from typing import List, Optional

from pydantic import Field

from src.models import BaseModelConfig, Vacation, Limit
from src.states.state_machine import MAIN_MENU


class UserData(BaseModelConfig):
    user_id: str = Field(..., description="Unique identifier for the user")
    state: str = Field(default=MAIN_MENU, description="Current state of the user in the bot")
    last_bot_message_id: Optional[str] = Field(None, description="ID of the last message_callbacks sent to the user")
    vacations: List[Vacation] = Field(default_factory=list, description="List of vacations associated with the user")
    limits: List[Limit] = Field(default_factory=list, description="List of current vacation limits for the user")
    current_vacation: Optional[Vacation] = Field(None, description="The current vacation being processed or edited")
    current_limit: Optional[Limit] = Field(None, description="The current vacation limit being processed or edited")
    new_vacation_dates: Optional[tuple[datetime, datetime]] = Field(None, description="New proposed vacation dates")
