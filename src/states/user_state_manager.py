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
