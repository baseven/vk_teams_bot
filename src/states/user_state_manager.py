import logging
from typing import Optional, Tuple
from datetime import datetime

from src.services.user_state import UserStateDatabaseService as DatabaseService
from src.models import UserState, Vacation, VacationType, VacationStatus
from src.states.state_machine import UserStateMachine

logger = logging.getLogger(__name__)


class UserStateManager:
    """Class responsible for managing user's state and vacations."""

    def __init__(self, user_state: UserState, database_service: Optional[DatabaseService] = None) -> None:
        """
        Initializes the UserStateManager with a given user state and database service.

        Args:
            user_state (UserState): The state of the user, which includes current vacations and limits.
            database_service (Optional[DatabaseService]): The service for interacting with the database.
        """
        self.user_state = user_state
        self.database_service = database_service or DatabaseService()
        self.state_machine = UserStateMachine(initial_state=self.user_state.state)
        logger.debug(f"Initialized UserStateManager for user {user_state.user_id}")

    def save_state(self) -> None:
        """
        Saves the current state of the user to the database.
        """
        self.user_state.state = self.state_machine.machine.state
        self.database_service.save_user_state(self.user_state)
        logger.info(f"State saved for user {self.user_state.user_id}: {self.user_state.state}")

    @classmethod
    def get_state(cls, user_id: str, database_service: Optional[DatabaseService] = None) -> 'UserStateManager':
        """
        Fetches the user's state from the database or initializes a new state if not found.

        Args:
            user_id (str): The unique identifier of the user.
            database_service (Optional[DatabaseService]): The database service to use for fetching the state.

        Returns:
            UserStateManager: An instance of UserStateManager initialized with the user's state.
        """
        database_service = database_service or DatabaseService()
        user_state = database_service.get_user_state(user_id)
        if not user_state:
            user_state = cls._initialize_new_user(user_id=user_id, database_service=database_service)
            logger.info(f"New state initialized for user {user_id}")
        else:
            logger.debug(f"Fetched existing state for user {user_id}")
        return cls(user_state=user_state, database_service=database_service)

    @staticmethod
    def _initialize_new_user(user_id: str, database_service: Optional[DatabaseService]) -> UserState:
        """
        Initializes a new user state and saves it to the database.

        Args:
            user_id (str): The unique identifier of the user.
            database_service (Optional[DatabaseService]): The service for interacting with the database.

        Returns:
            UserState: A new user state object.
        """
        new_user_state = UserState(user_id=user_id)
        database_service.save_user_state(new_user_state)
        logger.info(f"New user state created for {user_id}")
        return new_user_state

    def create_new_vacation(
            self,
            vacation_type: VacationType,
            start_date: str,
            end_date: str,
            status: VacationStatus = VacationStatus.PLANNED
    ) -> Vacation:
        """
        Creates a new vacation and sets it as the current vacation.

        Args:
            vacation_type (VacationType): The type of vacation.
            start_date (str): Start date in 'DD.MM.YYYY' format.
            end_date (str): End date in 'DD.MM.YYYY' format.
            status (VacationStatus): The status of the vacation (default is PLANNED).

        Returns:
            Vacation: The newly created vacation.
        """
        start_date_dt = datetime.strptime(start_date, "%d.%m.%Y")
        end_date_dt = datetime.strptime(end_date, "%d.%m.%Y")
        new_vacation = Vacation(
            vacation_type=vacation_type,
            start_date=start_date_dt,
            end_date=end_date_dt,
            status=status
        )
        self.user_state.current_vacation = new_vacation
        self._set_current_limit(vacation_type)
        logger.info(f"New vacation created for user {self.user_state.user_id}: "
                    f"{start_date_dt.strftime('%d.%m.%Y')} - {end_date_dt.strftime('%d.%m.%Y')}")
        return new_vacation

    def _set_current_limit(self, vacation_type: VacationType) -> None:
        """
        Finds and sets the current vacation limit for the given vacation type.

        Args:
            vacation_type (VacationType): The type of vacation for which to set the limit.
        """
        for limit in self.user_state.limits:
            if limit.vacation_type == vacation_type:
                self.user_state.current_limit = limit
                logger.debug(f"Vacation limit set for user {self.user_state.user_id}: "
                             f"{limit.available_days} days for {vacation_type}")
                return

        self.user_state.current_limit = None
        logger.warning(f"No vacation limit found for user {self.user_state.user_id} "
                       f"and vacation type {vacation_type}")

    def set_current_vacation(self, vacation_id: str) -> Optional[Vacation]:
        """
        Sets the current vacation (current_vacation) by vacation_id and applies the corresponding limit.

        Args:
            vacation_id (str): Unique identifier for the vacation.

        Returns:
            Optional[Vacation]: The found vacation or None if no matching vacation was found.
        """
        vacation = next((vac for vac in self.user_state.vacations if vac.vacation_id == vacation_id), None)

        if vacation:
            self.user_state.current_vacation = vacation
            self._set_current_limit(vacation.vacation_type)
            logger.info(f"Current vacation set for user {self.user_state.user_id}: {vacation_id}")
            return vacation

        logger.warning(f"Vacation with ID {vacation_id} not found for user {self.user_state.user_id}")

    def get_current_vacation(self) -> Optional[Vacation]:
        """
        Returns the current vacation being processed or edited.

        Returns:
            Optional[Vacation]: The current vacation, or None if no vacation is set.
        """
        return self.user_state.current_vacation

    def get_current_vacation_dates(self) -> Optional[Tuple[str, str]]:
        """
        Returns the dates of the current vacation as a tuple (start_date, end_date) in 'DD.MM.YYYY' format.

        Returns:
            Optional[Tuple[str, str]]: Tuple with the start and end dates of the current vacation,
            or None if no current vacation is set.
        """
        if self.user_state.current_vacation:
            start_date = self.user_state.current_vacation.start_date.strftime("%d.%m.%Y")
            end_date = self.user_state.current_vacation.end_date.strftime("%d.%m.%Y")
            logger.debug(f"Fetched vacation dates for user {self.user_state.user_id}: {start_date} - {end_date}")
            return start_date, end_date

        logger.warning(f"No current vacation set for user {self.user_state.user_id}")

    def set_last_bot_message_id(self, message_id: str) -> None:
        """
        Sets the ID of the last message sent by the bot to the user.

        Args:
            message_id (str): The ID of the last message.
        """
        self.user_state.last_bot_message_id = message_id
        logger.debug(f"Last bot message ID set for user {self.user_state.user_id}: {message_id}")

    def get_last_bot_message_id(self) -> Optional[str]:
        """
        Returns the ID of the last message sent by the bot to the user.

        Returns:
            Optional[str]: The ID of the last message or None if no message ID is set.
        """
        return self.user_state.last_bot_message_id

    def reset_current_vacation_and_limit(self) -> None:
        """
        Resets the current vacation (current_vacation) and the vacation limit (current_limit).

        After this method is called, both current_vacation and current_limit will be set to None.
        """
        self.user_state.current_vacation = None
        self.user_state.current_limit = None
        logger.info(f"Current vacation and limit reset for user {self.user_state.user_id}")
