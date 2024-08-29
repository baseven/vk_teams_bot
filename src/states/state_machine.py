import logging
from transitions import Machine

from services.database_service import DatabaseService
from models.user_state import UserState
from src.states.annual_vacation import annual_vacation_states, annual_vacation_transitions
from src.states.reschedule_vacation import reschedule_vacation_states, reschedule_vacation_transitions
from src.states.cancel_vacation import cancel_vacation_states, cancel_vacation_transitions

# Constants for states and triggers
MAIN_MENU = 'main_menu'
UNPAID_VACATION = 'unpaid_vacation'
VIEW_LIMITS_AND_SCHEDULE = 'view_limits_and_schedule'

TO_MAIN_MENU = 'to_main_menu'
TO_ANNUAL_VACATION_MENU = 'to_annual_vacation_menu'
TO_UNPAID_VACATION = 'to_unpaid_vacation'
TO_VIEW_LIMITS_AND_SCHEDULE = 'to_view_limits_and_schedule'
TO_RESCHEDULE_VACATION_MENU = 'to_reschedule_vacation_menu'
TO_CANCEL_VACATION_MENU = 'to_cancel_vacation_menu'

# Configure logging
logger = logging.getLogger(__name__)

# Define states and transitions outside the class
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

    def __init__(self, user_id, initial_state=MAIN_MENU, last_message_id=None, start_date=None, end_date=None,
                 database_service=None):
        """
        Initialize the bot state machine.

        Args:
            user_id (str): ID of the user.
            initial_state (str): Initial state of the bot.
            last_message_id (str, optional): ID of the last message.
            start_date (str, optional): Start date for vacation.
            end_date (str, optional): End date for vacation.
            database_service (DatabaseService, optional): Service for database operations.
        """
        self.user_id = user_id
        self.state = initial_state
        self.last_message_id = last_message_id
        self.start_date = start_date
        self.end_date = end_date
        self.database_service = database_service or DatabaseService()
        self.machine = Machine(model=self,
                               states=STATES,
                               transitions=TRANSITIONS,
                               initial=initial_state)

    def save_state(self):
        """Save the current state of the user to the database."""
        user_state = UserState(
            user_id=self.user_id,
            state=self.state,
            last_message_id=self.last_message_id,
            start_date=self.start_date,
            end_date=self.end_date
        )
        self.database_service.save_state(user_state)
        logger.info(f"State for user {self.user_id} saved: {self.state}")

    @classmethod
    def load_state(cls, user_id, database_service=None):
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
        return cls(
            user_id=user_id,
            initial_state=user_state.state,
            last_message_id=user_state.last_message_id,
            start_date=user_state.start_date,
            end_date=user_state.end_date,
            database_service=database_service
        )

    def set_vacation_dates(self, vacation_dates):
        """Set start_date and end_date based on the vacation_dates string."""
        try:
            start_date, end_date = vacation_dates.split(" - ")
            self.start_date = start_date
            self.end_date = end_date
            logger.info(f"Vacation dates set: {self.start_date} to {self.end_date}")
        except ValueError:
            logger.error("Invalid format for vacation dates. Expected format 'start_date - end_date'.")

    def get_vacation_dates(self) -> str:
        """Return the vacation dates as a string in the format 'start_date - end_date'."""
        if self.start_date and self.end_date:
            return f"{self.start_date} - {self.end_date}"
        else:
            return "Vacation dates are not set"

    def reset_vacation_dates(self):
        """Reset start_date and end_date to None."""
        self.start_date = None
        self.end_date = None
        logger.info("Vacation dates have been reset to None.")
