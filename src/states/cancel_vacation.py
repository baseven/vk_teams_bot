from enum import Enum
from transitions import State
from src.states.main_menu import MainMenu


class Triggers(Enum):
    """Triggers for state transitions in the Cancel Vacation process."""
    TO_SELECT_VACATION_TO_CANCEL = 'to_select_vacation_to_cancel'
    TO_CONFIRM_VACATION_CANCELLATION = 'to_confirm_vacation_cancellation'

class CancelVacation:
    """Class representing the states and transitions for the Cancel Vacation process."""
    select_vacation_to_cancel = State(name='select_vacation_to_cancel')
    confirm_vacation_cancellation = State(name='confirm_vacation_cancellation')

    states = [
        select_vacation_to_cancel,
        confirm_vacation_cancellation,
    ]

    transitions = [
        {
            'trigger': Triggers.TO_SELECT_VACATION_TO_CANCEL.value,
            'source': MainMenu.cancel_vacation_menu,
            'dest': select_vacation_to_cancel
        },
        {
            'trigger': Triggers.TO_CONFIRM_VACATION_CANCELLATION.value,
            'source': select_vacation_to_cancel,
            'dest': confirm_vacation_cancellation
        },

    ]
