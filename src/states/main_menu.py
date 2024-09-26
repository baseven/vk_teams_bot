from transitions import State

from src.actions.main_menu import MainMenuActions as Actions
from src.states.state_menu_base import StateMenuBase

class MainMenuTriggers:
    """Class containing all triggers for the main menu."""
    TO_MAIN_MENU = 'to_main_menu'
    TO_ANNUAL_VACATION_MENU = 'to_annual_vacation_menu'
    TO_UNPAID_VACATION = 'to_unpaid_vacation_menu'
    LIMITS_AND_VACATIONS_MENU = 'to_limits_and_vacations_menu'
    TO_RESCHEDULE_VACATION_MENU = 'to_reschedule_vacation_menu'
    TO_CANCEL_VACATION_MENU = 'to_cancel_vacation_menu'


class MainMenu(StateMenuBase):
    """Class representing the states and transitions for the main menu."""
    initial_state = 'main_menu'
    #TODO: try without .callback_data
    main_menu = State(name=initial_state)
    annual_vacation_menu = State(name=Actions.ANNUAL_VACATION_MENU.callback_data)
    unpaid_vacation_menu = State(name=Actions.UNPAID_VACATION_MENU.callback_data)
    limits_and_vacations_menu = State(name=Actions.LIMITS_AND_VACATIONS_MENU.callback_data)
    reschedule_vacation_menu = State(name=Actions.RESCHEDULE_VACATION_MENU.callback_data)
    cancel_vacation_menu = State(name=Actions.CANCEL_VACATION_MENU.callback_data)

    # Define state list and transitions
    _states = [
        main_menu,
        annual_vacation_menu,
        unpaid_vacation_menu,
        limits_and_vacations_menu,
        reschedule_vacation_menu,
        cancel_vacation_menu,
    ]

    #TODO: try without .name
    _transitions = [
        {
            'trigger': MainMenuTriggers.TO_ANNUAL_VACATION_MENU,
            'source': main_menu.name,
            'dest': annual_vacation_menu.name
        },
        {
            'trigger': MainMenuTriggers.TO_UNPAID_VACATION,
            'source': main_menu.name,
            'dest': unpaid_vacation_menu.name
        },
        {
            'trigger': MainMenuTriggers.LIMITS_AND_VACATIONS_MENU,
            'source': main_menu.name,
            'dest': limits_and_vacations_menu.name
        },
        {
            'trigger': MainMenuTriggers.TO_RESCHEDULE_VACATION_MENU,
            'source': main_menu.name,
            'dest': reschedule_vacation_menu.name
        },
        {
            'trigger': MainMenuTriggers.TO_CANCEL_VACATION_MENU,
            'source': main_menu.name,
            'dest': cancel_vacation_menu.name
        },
        {
            'trigger': MainMenuTriggers.TO_MAIN_MENU,
            'source': '*',
            'dest': main_menu.name
        },
    ]
