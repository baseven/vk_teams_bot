import logging
from typing import List, Optional
from datetime import datetime

from transitions import Machine

from services.database_service import DatabaseService
from models.user_state import UserState, Vacation, VacationType, VacationStatus
from src.states.annual_vacation import annual_vacation_states, annual_vacation_transitions
from src.states.reschedule_vacation import reschedule_vacation_states, reschedule_vacation_transitions
from src.states.cancel_vacation import cancel_vacation_states, cancel_vacation_transitions

# Константы для состояний и триггеров
MAIN_MENU = 'main_menu'
UNPAID_VACATION = 'unpaid_vacation'
VIEW_LIMITS_AND_SCHEDULE = 'view_limits_and_schedule'

TO_MAIN_MENU = 'to_main_menu'
TO_ANNUAL_VACATION_MENU = 'to_annual_vacation_menu'
TO_UNPAID_VACATION = 'to_unpaid_vacation'
TO_VIEW_LIMITS_AND_SCHEDULE = 'to_view_limits_and_schedule'
TO_RESCHEDULE_VACATION_MENU = 'to_reschedule_vacation_menu'
TO_CANCEL_VACATION_MENU = 'to_cancel_vacation_menu'

# Настройка логгирования
logger = logging.getLogger(__name__)

# Определение состояний и переходов
STATES = [
    MAIN_MENU,
    *annual_vacation_states,
    UNPAID_VACATION,
    VIEW_LIMITS_AND_SCHEDULE,
    *reschedule_vacation_states,
    *cancel_vacation_states
]

TRANSITIONS = [
    {'trigger': TO_MAIN_MENU, 'source': '*', 'dest': MAIN_MENU},
    {'trigger': TO_ANNUAL_VACATION_MENU, 'source': MAIN_MENU, 'dest': 'annual_vacation_menu'},
    {'trigger': TO_UNPAID_VACATION, 'source': MAIN_MENU, 'dest': UNPAID_VACATION},
    {'trigger': TO_VIEW_LIMITS_AND_SCHEDULE, 'source': MAIN_MENU, 'dest': VIEW_LIMITS_AND_SCHEDULE},
    {'trigger': TO_RESCHEDULE_VACATION_MENU, 'source': MAIN_MENU, 'dest': 'reschedule_vacation_menu'},
    {'trigger': TO_CANCEL_VACATION_MENU, 'source': MAIN_MENU, 'dest': 'cancel_vacation_menu'},
] + annual_vacation_transitions + reschedule_vacation_transitions + cancel_vacation_transitions


class BotStateMachine:
    """State machine for handling bot states and transitions."""

    def __init__(self, user_state: UserState, database_service: Optional[DatabaseService] = None):
        """
        Initialize the bot state machine.

        Args:
            user_state (UserState): The current user state instance.
            database_service (DatabaseService, optional): Service for database operations.
        """
        self.user_state = user_state
        self.database_service = database_service or DatabaseService()
        self.machine = Machine(
            model=self,
            states=STATES,
            transitions=TRANSITIONS,
            initial=self.user_state.state
        )

    def save_state(self) -> None:
        """
        Save the current state of the user to the database.
        """
        self.database_service.save_state(self.user_state)
        logger.info(f"State for user {self.user_state.user_id} saved: {self.user_state.state}")

    @classmethod
    def get_state(cls, user_id: str, database_service: Optional[DatabaseService] = None) -> 'BotStateMachine':
        """
        Get the user's state from the database, or create a new state if not found.

        Args:
            user_id (str): ID of the user.
            database_service (DatabaseService, optional): Service for database operations.
                                                          If None, a new instance of DatabaseService is created.

        Returns:
            BotStateMachine: Instance of the state machine with loaded or newly initialized state.
        """
        database_service = database_service or DatabaseService()
        user_state = database_service.get_user_state(user_id)
        if not user_state:
            user_state = cls._initialize_new_user_state(user_id=user_id, database_service=database_service)
        return cls(user_state=user_state, database_service=database_service)

    @staticmethod
    def _initialize_new_user_state(user_id: str, database_service: Optional[DatabaseService]) -> UserState:
        """
        Initialize a new user state and save it to the database.

        Args:
            user_id (str): ID of the user.
            database_service (DatabaseService): Service for database operations.

        Returns:
            UserState: The newly initialized user state.
        """
        new_user_state = UserState(
            user_id=user_id,
            state=MAIN_MENU
        )
        database_service.save_state(new_user_state)
        logger.info(f"New user state initialized and saved for user {user_id} with state: '{MAIN_MENU}'")
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

        # Создаем новый отпуск без vacation_id (он будет присвоен в БД)
        new_vacation = Vacation(
            vacation_type=vacation_type,
            start_date=start_date_dt,
            end_date=end_date_dt,
            status=status
        )

        self.user_state.current_vacation = new_vacation
        self._set_current_vacation_limit(vacation_type)
        logger.info(f"New vacation created: {new_vacation.start_date} - {new_vacation.end_date}")

        return new_vacation

    def _set_current_vacation_limit(self, vacation_type: VacationType) -> None:
        """
        Find and set the current vacation limit for the given vacation type.

        Args:
            vacation_type (VacationType): The type of vacation for which to set the limit.

        Returns:
            None
        """
        # Поиск лимита для данного типа отпуска
        for limit in self.user_state.vacation_limits:
            if limit.vacation_type == vacation_type:
                self.user_state.current_vacation_limit = limit
                logger.info(
                    f"Vacation limit set for vacation type {vacation_type}: {limit.available_days} days available.")
                return

        # Если лимит не найден, сбрасываем current_vacation_limit
        self.user_state.current_vacation_limit = None
        logger.warning(f"No vacation limit found for vacation type {vacation_type}.")

        def get_current_vacation_info(self) -> Optional[dict]:
            """
            Get a summary of the current vacation for display.
            """
            current_vacation = self.user_state.current_vacation
            if current_vacation:
                return {
                    "vacation_type": current_vacation.vacation_type.value,
                    "start_date": current_vacation.start_date.strftime('%Y-%m-%d'),
                    "end_date": current_vacation.end_date.strftime('%Y-%m-%d'),
                    "status": current_vacation.status.value
                }
            else:
                logger.warning("No current vacation is set.")
                return None

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
