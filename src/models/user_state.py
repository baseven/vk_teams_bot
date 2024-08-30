from pydantic import BaseModel, Field
from typing import List, Optional
from src.models.vacation import Vacation, Limit, VacationType  # Объединенный импорт моделей и типов


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

    # def add_vacation(self, vacation: Vacation):
    #     """Add a new vacation to the user's list of vacations."""
    #     self.vacations.append(vacation)
    #     self.current_vacation = vacation  # Обновляем текущее значение отпуска

    def get_vacation_by_id(self, vacation_id: str) -> Optional[Vacation]:
        """Retrieve a vacation by its ID."""
        for vacation in self.vacations:
            if vacation.vacation_id == vacation_id:
                self.current_vacation = vacation  # Устанавливаем текущий отпуск
                return vacation
        self.current_vacation = None  # Если не найдено, сбрасываем текущее значение отпуска
        return None

    # def update_vacation_limit(self, vacation_type: VacationType, days_used: int):
    #     """
    #     Update the vacation limit by reducing the available days for a specific type of vacation.
    #
    #     Args:
    #         vacation_type (VacationType): The type of vacation to update.
    #         days_used (int): The number of days used to subtract from the available days.
    #     """
    #     for vacation_limit in self.vacation_limits:
    #         if vacation_limit.vacation_type == vacation_type:
    #             if vacation_limit.available_days is not None and vacation_limit.available_days >= days_used:
    #                 vacation_limit.available_days -= days_used
    #                 self.current_vacation_limit = vacation_limit  # Обновляем текущее значение лимита
    #             else:
    #                 raise ValueError("Insufficient vacation days available.")
    #             break
    #     else:
    #         self.current_vacation_limit = None  # Если не найдено, сбрасываем текущее значение лимита
    #         raise ValueError(f"Vacation type '{vacation_type}' not found.")

    class Config:
        validate_assignment = True  # Automatically validate fields on assignment
