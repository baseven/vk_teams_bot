import logging

from transitions import Machine

from src.states.annual_vacation import AnnualVacation
from src.states.main_menu import MainMenu
from src.states.cancel_vacation import CancelVacation
from src.states.reschedule_vacation import RescheduleVacation

logger = logging.getLogger(__name__)

STATES = MainMenu.states + AnnualVacation.states + CancelVacation.states + RescheduleVacation.states
logger.debug(f'States: {STATES}')

TRANSITIONS = (MainMenu.transitions + AnnualVacation.transitions + CancelVacation.transitions +
               RescheduleVacation.transitions)
logger.debug(f'TRANSITIONS: {TRANSITIONS}')


class StateMachine:
    """State machine for handling bot states and transitions."""

    def __init__(self, initial_state: str):
        """Initialize the bot state machine."""
        self.state = initial_state
        self.machine = Machine(
            model=self,
            states=STATES,
            transitions=TRANSITIONS,
            initial=initial_state
        )
