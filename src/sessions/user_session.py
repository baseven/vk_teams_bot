import logging

from typing import Optional

from src.temporary_data.vacations import limits, vacations
from src.sessions.managers.vacation_manager import VacationManager
from src.models import UserData
from src.services import UserDataDatabaseService as DatabaseService
from src.states import StateMachine

logger = logging.getLogger(__name__)


class UserSession:
    """Class responsible for managing user's session and associated data."""

    def __init__(self, user_id: str, database_service: Optional[DatabaseService] = None) -> None:
        """
        Initializes the UserSession with a given user data and database service.

        Args:
            user_id (str): The unique identifier of the user.
            database_service (Optional[DatabaseService]): The service for interacting with the database.
        """
        self.database_service = database_service or DatabaseService()
        self.user_data = self._get_or_create_user_data(user_id)
        self.state_machine = StateMachine(initial_state=self.user_data.state)
        self.vacation_manager = VacationManager(self.user_data)

    @property
    def last_bot_message_id(self) -> Optional[str]:
        return self.user_data.last_bot_message_id

    @last_bot_message_id.setter
    def last_bot_message_id(self, message_id: str) -> None:
        self.user_data.last_bot_message_id = message_id

    @property
    def state(self) -> str:
        return self.user_data.state

    @state.setter
    def state(self, state: str) -> None:
        self.user_data.state = state

    def _get_or_create_user_data(self, user_id: str) -> UserData:
        """
        Retrieves the user's data from the database or creates new data if not found.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            UserData: The user's data.
        """
        user_data = self.database_service.get_user_data(user_id)
        if user_data is None:
            user_data = self._initialize_new_user_data(user_id)
            logger.debug(f"New session initialized for user {user_id}")
        else:
            logger.debug(f"Fetched existing session for user {user_id}")
        return user_data

    def _initialize_new_user_data(self, user_id: str) -> UserData:
        """
        Creates new user data and saves it to the database.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            UserData: The new user's data.
        """
        #TODO: Currently, vacation limits and schedule are loaded from static data files.
        # In the future, this data will be fetched from the database.
        # vacations =
        # limits =

        new_user_data = UserData(
            user_id=user_id,
            vacations=vacations,
            limits=limits,
        )
        self.database_service.save_user_data(new_user_data)
        logger.info(f"New user data created for user {user_id}")
        return new_user_data

    def save_session(self) -> None:
        """
         Saves the current user session to the database.
         """
        self.state = self.state_machine.state
        self.database_service.save_user_data(self.user_data)
        logger.info(f"Session for user {self.user_data.user_id} saved with state: {self.user_data.state}")
