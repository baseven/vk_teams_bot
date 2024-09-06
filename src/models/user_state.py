from pydantic import BaseModel, Field
from typing import List, Optional
from src.models.vacation import Vacation, Limit, VacationType, VacationStatus  # Объединенный импорт моделей и типов


class UserState(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    state: str = Field(..., description="Current state of the user in the bot")
    last_message_id: Optional[str] = Field(None, description="ID of the last message sent to the user")
    vacations: List[Vacation] = Field(default_factory=list, description="List of vacations associated with the user")
    vacation_limits: List[Limit] = Field(default_factory=list,
                                         description="List of current vacation limits for the user")

    # Новые поля для текущего отпуска и текущего лимита доступных дней
    current_vacation: Optional[Vacation] = Field(None, description="The current vacation being processed or edited")
    current_vacation_limit: Optional[Limit] = Field(None,
                                                    description="The current vacation limit being processed or edited")

    def get_vacation_by_id(self, vacation_id: str) -> Optional[Vacation]:
        """Retrieve a vacation by its ID."""
        for vacation in self.vacations:
            if vacation.vacation_id == vacation_id:
                self.current_vacation = vacation  # Устанавливаем текущий отпуск
                return vacation
        self.current_vacation = None  # Если не найдено, сбрасываем текущее значение отпуска
        return None

    class Config:
        validate_assignment = True  # Automatically validate fields on assignment
