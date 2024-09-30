from enum import Enum
from transitions import State
from src.states.main_menu import MainMenu


class Triggers(Enum):
    """Triggers for state transitions in the Reschedule Vacation process."""
    TO_CONFIRM_VACATION_SELECTION = 'to_confirm_vacation_selection'
    TO_ENTER_NEW_VACATION_DATES = 'to_enter_new_vacation_dates'
    TO_CONFIRM_VACATION_RESCHEDULE = 'to_confirm_vacation_reschedule'

class RescheduleVacation:
    """Class representing the states and transitions for the Reschedule Vacation process."""
    confirm_vacation_selection = State(name='confirm_vacation_selection')
    enter_new_vacation_dates = State(name='enter_new_vacation_dates')
    confirm_vacation_reschedule = State(name='confirm_vacation_reschedule')

    states = [
        confirm_vacation_selection,
        enter_new_vacation_dates,
        confirm_vacation_reschedule,
    ]

    transitions = [
        {
            'trigger': Triggers.TO_CONFIRM_VACATION_SELECTION.value,
            'source': MainMenu.reschedule_vacation_menu,
            'dest': confirm_vacation_selection
        },
        {
            'trigger': Triggers.TO_ENTER_NEW_VACATION_DATES.value,
            'source': confirm_vacation_selection,
            'dest': enter_new_vacation_dates
        },
        {
            'trigger': Triggers.TO_CONFIRM_VACATION_RESCHEDULE.value,
            'source': enter_new_vacation_dates,
            'dest': confirm_vacation_reschedule
        },
    ]
