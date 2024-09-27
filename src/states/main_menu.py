from enum import Enum
from transitions import State


class Triggers(Enum):
    """Triggers for state transitions in the main menu."""
    TO_ANNUAL_VACATION_MENU = 'to_annual_vacation_menu'
    TO_UNPAID_VACATION_MENU = 'to_unpaid_vacation_menu'
    TO_LIMITS_AND_VACATIONS_MENU = 'to_limits_and_vacations_menu'
    TO_RESCHEDULE_VACATION_MENU = 'to_reschedule_vacation_menu'
    TO_CANCEL_VACATION_MENU = 'to_cancel_vacation_menu'
    TO_MAIN_MENU = 'to_main_menu'

class MainMenu:
    """Class representing the states and transitions for the main menu."""
    main_menu = State(name='main_menu')
    annual_vacation_menu = State(name='annual_vacation_menu')
    unpaid_vacation_menu = State(name='unpaid_vacation_menu')
    limits_and_vacations_menu = State(name='limits_and_vacations_menu')
    reschedule_vacation_menu = State(name='reschedule_vacation_menu')
    cancel_vacation_menu = State(name='cancel_vacation_menu')

    states = [
        main_menu,
        annual_vacation_menu,
        unpaid_vacation_menu,
        limits_and_vacations_menu,
        reschedule_vacation_menu,
        cancel_vacation_menu,
    ]

    transitions = [
        {
            'trigger': Triggers.TO_ANNUAL_VACATION_MENU.value,
            'source': main_menu,
            'dest': annual_vacation_menu
        },
        {
            'trigger': Triggers.TO_UNPAID_VACATION_MENU.value,
            'source': main_menu,
            'dest': unpaid_vacation_menu
        },
        {
            'trigger': Triggers.TO_LIMITS_AND_VACATIONS_MENU.value,
            'source': main_menu,
            'dest': limits_and_vacations_menu
        },
        {
            'trigger': Triggers.TO_RESCHEDULE_VACATION_MENU.value,
            'source': main_menu,
            'dest': reschedule_vacation_menu
        },
        {
            'trigger': Triggers.TO_CANCEL_VACATION_MENU.value,
            'source': main_menu,
            'dest': cancel_vacation_menu
        },
        {
            'trigger': Triggers.TO_MAIN_MENU.value,
            'source': '*',
            'dest': main_menu
        },
    ]

    initial_state = main_menu
