import logging
from typing import List, Optional
from transitions import Machine
from services.database_service import DatabaseService
from models.user_state import UserState, Vacation, VacationType, VacationStatus
from src.states.annual_vacation import annual_vacation_states, annual_vacation_transitions
from src.states.reschedule_vacation import reschedule_vacation_states, reschedule_vacation_transitions
from src.states.cancel_vacation import cancel_vacation_states, cancel_vacation_transitions
from datetime import datetime

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

    def __init__(self, user_state: UserState, database_service=None):
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

    def save_state(self):
        """Save the current state of the user to the database."""
        self.database_service.save_state(self.user_state)
        logger.info(f"State for user {self.user_state.user_id} saved: {self.user_state.state}")

    @classmethod
    def load_state(cls, user_id: str, database_service=None):
        """
        Load the state of the user from the database.

        Args:
            user_id (str): ID of the user.
            database_service (DatabaseService, optional): Service for database operations.

        Returns:
            BotStateMachine: Instance of the state machine with loaded state.
        """
        database_service = database_service or DatabaseService()
        user_state = database_service.load_state(user_id)
        logger.info(f"State for user {user_id} loaded: {user_state.state}")
        return cls(user_state=user_state, database_service=database_service)

    def initialize_current_vacation(self, vacation_type: VacationType, start_date: str, end_date: str,
                                    status: VacationStatus = VacationStatus.PLANNED, vacation_id: Optional[str] = None):
        """
        Initialize or update the current vacation being processed.

        Args:
            vacation_type (VacationType): Type of the vacation.
            start_date (str): Start date of the vacation in 'YYYY-MM-DD' format.
            end_date (str): End date of the vacation in 'YYYY-MM-DD' format.
            status (VacationStatus): Status of the vacation (default is PLANNED).
            vacation_id (str, optional): ID of the vacation, if modifying an existing one.
        """
        try:
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

            # Если vacation_id не предоставлен, создаем новый отпуск
            if not vacation_id:
                new_vacation = Vacation(
                    vacation_id=None,  # ID будет присвоен после сохранения в БД
                    vacation_type=vacation_type,
                    start_date=start_date_dt,
                    end_date=end_date_dt,
                    status=status
                )
                self.user_state.current_vacation = new_vacation
                self.user_state.vacations.append(new_vacation)
                logger.info(f"Initialized new vacation: {new_vacation.start_date} to {new_vacation.end_date}")
            else:
                # Если vacation_id предоставлен, ищем и обновляем существующий отпуск
                vacation = self.user_state.get_vacation_by_id(vacation_id)
                if vacation:
                    vacation.start_date = start_date_dt
                    vacation.end_date = end_date_dt
                    vacation.vacation_type = vacation_type
                    vacation.status = status
                    logger.info(
                        f"Updated existing vacation {vacation_id}: {vacation.start_date} to {vacation.end_date}")
                else:
                    logger.warning(f"Vacation with ID {vacation_id} not found. Creating a new vacation.")
                    new_vacation = Vacation(
                        vacation_id=None,  # ID будет присвоен после сохранения в БД
                        vacation_type=vacation_type,
                        start_date=start_date_dt,
                        end_date=end_date_dt,
                        status=status
                    )
                    self.user_state.current_vacation = new_vacation
                    self.user_state.vacations.append(new_vacation)
                    logger.info(f"Initialized new vacation: {new_vacation.start_date} to {new_vacation.end_date}")

        except ValueError as e:
            logger.error(f"Error initializing vacation: {e}")

    def get_vacation_dates(self) -> str:
        """Return the vacation dates as a string in the format 'YYYY-MM-DD - YYYY-MM-DD'."""
        if self.user_state.current_vacation and self.user_state.current_vacation.start_date and self.user_state.current_vacation.end_date:
            return f"{self.user_state.current_vacation.start_date.strftime('%Y-%m-%d')} - {self.user_state.current_vacation.end_date.strftime('%Y-%m-%d')}"
        else:
            return "Vacation dates are not set"

    def reset_vacation_dates(self):
        """Reset start_date and end_date of the current vacation to None."""
        if self.user_state.current_vacation:
            self.user_state.current_vacation.start_date = None
            self.user_state.current_vacation.end_date = None
            logger.info("Vacation dates have been reset to None.")
