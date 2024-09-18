import logging

from typing import Optional
from datetime import datetime

from src.data.vacation_limits import vacation_limits
from src.data.vacation_schedule import vacation_schedule
from src.models import UserData, Vacation, Limit, VacationType, VacationStatus
from src.services import UserDataDatabaseService as DatabaseService
from src.states import StateMachine

logger = logging.getLogger(__name__)


class UserSession:
    """Class responsible for managing user's session and associated data."""

    def __init__(self, user_data: UserData, database_service: Optional[DatabaseService] = None) -> None:
        """
        Initializes the UserSession with a given user data and database service.

        Args:
            user_data (UserData): The data of the user, which includes current vacations and limits.
            database_service (Optional[DatabaseService]): The service for interacting with the database.
        """
        self.user_data = user_data
        self.database_service = database_service or DatabaseService()
        self.state_machine = StateMachine(initial_state=self.user_data.state)

    def save_session(self) -> None:
        """
        Save the current session of the user to the database.
        """
        self.user_data.state = self.state_machine.state
        self.database_service.save_user_data(self.user_data)
        logger.info(f"Session for user {self.user_data.user_id} saved: {self.user_data.state}")

    @classmethod
    def get_session(cls, user_id: str, database_service: Optional[DatabaseService] = None) -> 'UserSession':
        """
        Fetches the user's session from the database or initializes a new session if not found.

        Args:
            user_id (str): The unique identifier of the user.
            database_service (Optional[DatabaseService]): The database service to use for fetching the session.

        Returns:
            UserSession: An instance of UserSession initialized with the user's data.
        """
        database_service = database_service or DatabaseService()
        user_data = database_service.get_user_data(user_id)
        if not user_data:
            user_data = cls._initialize_new_user_data(user_id=user_id, database_service=database_service)
            logger.info(f"New session initialized for user {user_id}")
        else:
            logger.debug(f"Fetched existing session for user {user_id}")
        return cls(user_data=user_data, database_service=database_service)

    @staticmethod
    def _initialize_new_user_data(user_id: str, database_service: Optional[DatabaseService]) -> UserData:
        """
        Creates a new user profile and saves it to the database.

        Args:
            user_id (str): The unique identifier of the user.
            database_service (Optional[DatabaseService]): The service for interacting with the database.

        Returns:
            UserData: A new user data object.
        """
        #TODO:Currently, vacation limits and schedule are loaded from static data files.
        # In the future, this data will be fetched from the database.
        vacations = vacation_schedule
        limits = vacation_limits
        new_user_data = UserData(
            user_id=user_id,
            vacations=vacations,
            limits=limits,
        )
        database_service.save_user_data(new_user_data)
        logger.info(f"New user data created for {user_id}")
        return new_user_data

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
        self.user_data.current_vacation = new_vacation
        self._set_current_limit(vacation_type)
        logger.info(f"New vacation created for user {self.user_data.user_id}: "
                    f"{start_date_dt.strftime('%d.%m.%Y')} - {end_date_dt.strftime('%d.%m.%Y')}")
        return new_vacation

    def _set_current_limit(self, vacation_type: VacationType) -> None:
        """
        Finds and sets the current vacation limit for the given vacation type.

        Args:
            vacation_type (VacationType): The type of vacation for which to set the limit.
        """
        for limit in self.user_data.limits:
            if limit.vacation_type == vacation_type:
                self.user_data.current_limit = limit
                logger.debug(f"Vacation limit set for user {self.user_data.user_id}: "
                             f"{limit.available_days} days for {vacation_type}")
                return

        self.user_data.current_limit = None
        logger.warning(f"No vacation limit found for user {self.user_data.user_id} "
                       f"and vacation type {vacation_type}")

    def set_current_vacation(self, vacation_id: str) -> Optional[Vacation]:
        """
        Sets the current vacation by vacation_id and applies the corresponding limit.

        Args:
            vacation_id (str): Unique identifier for the vacation.

        Returns:
            Optional[Vacation]: The found vacation or None if no matching vacation was found.
        """
        vacation = next((vac for vac in self.user_data.vacations if vac.vacation_id == vacation_id), None)

        if vacation:
            self.user_data.current_vacation = vacation
            self._set_current_limit(vacation.vacation_type)
            logger.info(f"Current vacation set for user {self.user_data.user_id}: {vacation_id}")
            return vacation

        logger.warning(f"Vacation with ID {vacation_id} not found for user {self.user_data.user_id}")

    def get_current_vacation(self) -> Optional[Vacation]:
        """
        Returns the current vacation being processed or edited.

        Returns:
            Optional[Vacation]: The current vacation, or None if no vacation is set.
        """
        return self.user_data.current_vacation

    def get_current_vacation_dates(self) -> Optional[tuple[str, str]]:
        """
        Returns the dates of the current vacation as a tuple (start_date, end_date) in 'DD.MM.YYYY' format.

        Returns:
            Optional[tuple[str, str]]: Tuple with the start and end dates of the current vacation,
            or None if no current vacation is set.
        """
        if self.user_data.current_vacation:
            start_date = self.user_data.current_vacation.start_date.strftime("%d.%m.%Y")
            end_date = self.user_data.current_vacation.end_date.strftime("%d.%m.%Y")
            logger.debug(f"Fetched vacation dates for user {self.user_data.user_id}: {start_date} - {end_date}")
            return start_date, end_date

        logger.warning(f"No current vacation set for user {self.user_data.user_id}")

    def set_last_bot_message_id(self, message_id: str) -> None:
        """
        Sets the ID of the last message_callbacks sent by the bot to the user.

        Args:
            message_id (str): The ID of the last message_callbacks.
        """
        self.user_data.last_bot_message_id = message_id
        logger.debug(f"Last bot message_callbacks ID set for user {self.user_data.user_id}: {message_id}")

    def get_last_bot_message_id(self) -> Optional[str]:
        """
        Returns the ID of the last message_callbacks sent by the bot to the user.

        Returns:
            Optional[str]: The ID of the last message_callbacks or None if no message_callbacks ID is set.
        """
        return self.user_data.last_bot_message_id

    def reset_current_vacation_and_limit(self) -> None:
        """
        Resets the current vacation (current_vacation) and the vacation limit (current_limit).

        After this method is called, both current_vacation and current_limit will be set to None.
        """
        self.user_data.current_vacation = None
        self.user_data.current_limit = None
        logger.info(f"Current vacation and limit reset for user {self.user_data.user_id}")

    def set_new_vacation_dates(self, start_date: str, end_date: str) -> None:
        """
        Set new vacation dates for editing.

        Args:
            start_date (str): Start date in 'DD.MM.YYYY' format.
            end_date (str): End date in 'DD.MM.YYYY' format.

        Raises:
            ValueError: If the start date is later than the end date.
        """
        start_date_dt = datetime.strptime(start_date, "%d.%m.%Y")
        end_date_dt = datetime.strptime(end_date, "%d.%m.%Y")

        self.user_data.new_vacation_dates = (start_date_dt, end_date_dt)
        logger.info(f"New vacation dates set for user {self.user_data.user_id}: {start_date} - {end_date}")

    def get_new_vacation_dates(self) -> Optional[tuple[str, str]]:
        """
        Get the new vacation dates being edited as a tuple (start_date, end_date) in 'DD.MM.YYYY' format.

        Returns:
            Optional[tuple[str, str]]: Tuple with the start and end dates in 'DD.MM.YYYY' format,
            or None if no new vacation dates are set.
        """
        if self.user_data.new_vacation_dates:
            start_date, end_date = self.user_data.new_vacation_dates
            logger.debug(
                f"Fetched new vacation dates for user {self.user_data.user_id}: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}")
            return start_date.strftime("%d.%m.%Y"), end_date.strftime("%d.%m.%Y")

        logger.warning(f"No new vacation dates set for user {self.user_data.user_id}")
        return None

    def get_vacations_and_limits(self) -> tuple[list[Vacation], list[Limit]]:
        """
        Returns the user's vacations and limits as a tuple.

        Returns:
            tuple[list[Vacation], list[Limit]]: A tuple containing the list of vacations and the list of limits.
        """
        vacations = self.user_data.vacations
        limits = self.user_data.limits
        logger.debug(f"Returning vacations and limits for user {self.user_data.user_id}")
        return vacations, limits
