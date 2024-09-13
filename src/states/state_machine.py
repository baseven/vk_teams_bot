import logging

from transitions import Machine

from src.states.annual_vacation import annual_vacation_states, annual_vacation_transitions
from src.states.reschedule_vacation import reschedule_vacation_states, reschedule_vacation_transitions
from src.states.cancel_vacation import cancel_vacation_states, cancel_vacation_transitions

MAIN_MENU = 'main_menu'
UNPAID_VACATION = 'unpaid_vacation_menu'
VIEW_LIMITS_AND_SCHEDULE = 'view_limits_and_schedule'

TO_MAIN_MENU = 'to_main_menu'
TO_ANNUAL_VACATION_MENU = 'to_annual_vacation_menu'
TO_UNPAID_VACATION = 'to_unpaid_vacation_menu'
TO_VIEW_LIMITS_AND_SCHEDULE = 'to_view_limits_and_schedule'
TO_RESCHEDULE_VACATION_MENU = 'to_reschedule_vacation_menu'
TO_CANCEL_VACATION_MENU = 'to_cancel_vacation_menu'

logger = logging.getLogger(__name__)

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


class StateMachine:
    """State machine for handling bot states and transitions."""

    def __init__(self, initial_state: str = MAIN_MENU):
        """Initialize the bot state machine."""
        self.machine = Machine(
            model=self,
            states=STATES,
            transitions=TRANSITIONS,
            initial=initial_state
        )
