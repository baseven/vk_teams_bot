from enum import Enum
from transitions import State
from src.states.main_menu import MainMenu


class Triggers(Enum):
    """Triggers for state transitions in the Annual Vacation process."""
    TO_HANDLE_ANNUAL_VACATION = 'to_handle_annual_vacation'
    TO_CREATE_ANNUAL_VACATION = 'to_create_annual_vacation'
    TO_CONFIRM_ANNUAL_VACATION = 'to_confirm_annual_vacation'

class AnnualVacation:
    """Class representing the states and transitions for the Annual Vacation process."""
    handle_annual_vacation = State(name='handle_annual_vacation')
    create_annual_vacation = State(name='create_annual_vacation')
    confirm_annual_vacation = State(name='confirm_annual_vacation')

    states = [
        handle_annual_vacation,
        create_annual_vacation,
        confirm_annual_vacation,
    ]

    transitions = [
        {
            'trigger': Triggers.TO_HANDLE_ANNUAL_VACATION.value,
            'source': MainMenu.annual_vacation_menu,
            'dest': handle_annual_vacation
        },
        {
            'trigger': Triggers.TO_CREATE_ANNUAL_VACATION.value,
            'source': [MainMenu.annual_vacation_menu, handle_annual_vacation],
            'dest': create_annual_vacation
        },
        {
            'trigger': Triggers.TO_CONFIRM_ANNUAL_VACATION.value,
            'source': [handle_annual_vacation, create_annual_vacation],
            'dest': confirm_annual_vacation
        },
    ]
