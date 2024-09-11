import logging
from typing import Optional
from datetime import datetime

from src.services.user_state import UserStateDatabaseService as DatabaseService
from src.models import UserState, Vacation, VacationType, VacationStatus
from src.states.state_machine import UserStateMachine

logger = logging.getLogger(__name__)


class UserStateManager:
    """Class responsible for managing user's state and vacations."""

    def __init__(self, user_state: UserState, database_service: Optional[DatabaseService] = None):
        self.user_state = user_state
        self.database_service = database_service or DatabaseService()
        self.state_machine = UserStateMachine(initial_state=self.user_state.state)

    def save_state(self) -> None:
        """
        Save the current state of the user to the database.
        """
        self.user_state.state = self.state_machine.machine.state
        self.database_service.save_user_state(self.user_state)
        logger.info(f"State for user {self.user_state.user_id} saved: {self.user_state.state}")

    @classmethod
    def get_state(cls, user_id: str, database_service: Optional[DatabaseService] = None) -> 'UserStateManager':
        """
        Get the user's state from the database, or create a new state if not found.
        """
        database_service = database_service or DatabaseService()
        user_state = database_service.get_user_state(user_id)
        if not user_state:
            user_state = cls._initialize_new_user(user_id=user_id, database_service=database_service)
        return cls(user_state=user_state, database_service=database_service)

    @staticmethod
    def _initialize_new_user(user_id: str, database_service: Optional[DatabaseService]) -> UserState:
        """
        Initialize a new user state and save it to the database.
        """
        new_user_state = UserState(user_id=user_id)
        database_service.save_user_state(new_user_state)
        logger.info(f"New user state initialized and saved for user {user_id} with state: 'main_menu'")
        return new_user_state

    def create_new_vacation(
            self,
            vacation_type: VacationType,
            start_date: str,
            end_date: str,
            status: VacationStatus = VacationStatus.PLANNED
    ) -> Vacation:
        """
        Create a new vacation and set it as the current vacation.

        Args:
            vacation_type (VacationType): Type of the vacation.
            start_date (str): Start date of the vacation in 'YYYY-MM-DD' format.
            end_date (str): End date of the vacation in 'YYYY-MM-DD' format.
            status (VacationStatus): Status of the vacation (default is PLANNED).

        Returns:
            Vacation: The newly created vacation.
        """
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        new_vacation = Vacation(
            vacation_type=vacation_type,
            start_date=start_date_dt,
            end_date=end_date_dt,
            status=status
        )
        self.user_state.current_vacation = new_vacation
        self._set_current_limit(vacation_type)
        logger.info(f"New vacation created: {new_vacation.start_date} - {new_vacation.end_date}")
        return new_vacation

    def _set_current_limit(self, vacation_type: VacationType) -> None:
        """
        Find and set the current vacation limit for the given vacation type.

        Args:
            vacation_type (VacationType): The type of vacation for which to set the limit.

        Returns:
            None
        """
        for limit in self.user_state.limits:
            if limit.vacation_type == vacation_type:
                self.user_state.current_limit = limit
                logger.info(
                    f"Vacation limit set for vacation type {vacation_type}: {limit.available_days} days available.")
                return

        self.user_state.current_limit = None
        logger.warning(f"No vacation limit found for vacation type {vacation_type}.")

    def get_current_vacation(self) -> Optional[Vacation]:
        """
        Return the current vacation being processed or edited.

        Returns:
            Optional[Vacation]: The current vacation, or None if no vacation is set.
        """
        if self.user_state.current_vacation:
            return self.user_state.current_vacation
        else:
            logger.warning("No current vacation is set.")
            return None

    def set_current_vacation(self, vacation_id: str) -> Optional[Vacation]:
        """
        Устанавливает текущий отпуск (current_vacation) по идентификатору отпуска (vacation_id)
        и применяет текущий лимит отпуска.

        Args:
            vacation_id (str): Уникальный идентификатор отпуска.

        Returns:
            Optional[Vacation]: Найденный отпуск, или None, если отпуск не найден.
        """
        for vacation in self.user_state.vacations:
            if vacation.vacation_id == vacation_id:
                self.user_state.current_vacation = vacation
                self._set_current_limit(vacation.vacation_type)
                logger.info(f"Current vacation set to {vacation_id} for user {self.user_state.user_id}")
                return vacation

        logger.warning(f"Vacation with ID {vacation_id} not found for user {self.user_state.user_id}")
        return None

    def get_current_vacation_dates(self) -> Optional[tuple[datetime, datetime]]:
        """
        Возвращает даты текущего отпуска в виде кортежа (start_date, end_date).

        Returns:
            Optional[tuple[datetime, datetime]]: Кортеж с датами начала и окончания текущего отпуска,
            или None, если текущий отпуск не установлен.
        """
        if self.user_state.current_vacation:
            start_date = self.user_state.current_vacation.start_date
            end_date = self.user_state.current_vacation.end_date
            return start_date, end_date
        else:
            logger.warning("No current vacation is set.")
            return None

    def set_last_bot_message_id(self, message_id: str) -> None:
        """
        Устанавливает ID последнего сообщения, отправленного ботом пользователю.

        Args:
            message_id (str): ID сообщения, которое нужно установить как последнее.
        """
        self.user_state.last_bot_message_id = message_id
        logger.info(f"Last bot message ID set to {message_id} for user {self.user_state.user_id}")

    def get_last_bot_message_id(self) -> Optional[str]:
        """
        Возвращает ID последнего сообщения, отправленного ботом пользователю.

        Returns:
            Optional[str]: ID последнего сообщения или None, если сообщение не установлено.
        """
        return self.user_state.last_bot_message_id

    def reset_current_vacation_and_limit(self) -> None:
        """
        Сбрасывает текущий отпуск (current_vacation) и лимит отпуска (current_limit).

        После выполнения метода поля current_vacation и current_limit будут установлены в None.
        """
        self.user_state.current_vacation = None
        self.user_state.current_limit = None
        logger.info(f"Current vacation and limit reset for user {self.user_state.user_id}")
