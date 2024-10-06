from src.buttons.bot_button import BotButton
from src.states.main_menu import MainMenu
from src.texts.buttons import buttons


class MainMenuButtons:
    ANNUAL_VACATION_MENU = BotButton(
        callback_data=MainMenu.annual_vacation_menu.name,
        text=buttons.main_menu.ANNUAL_VACATION_MENU
    )
    UNPAID_VACATION_MENU = BotButton(
        callback_data=MainMenu.unpaid_vacation_menu.name,
        text=buttons.main_menu.UNPAID_VACATION_MENU
    )
    LIMITS_AND_VACATIONS_MENU = BotButton(
        callback_data=MainMenu.limits_and_vacations_menu.name,
        text=buttons.main_menu.LIMITS_AND_VACATIONS_MENU
    )
    RESCHEDULE_VACATION_MENU = BotButton(
        callback_data=MainMenu.reschedule_vacation_menu.name,
        text=buttons.main_menu.RESCHEDULE_VACATION_MENU
    )
    CANCEL_VACATION_MENU = BotButton(
        callback_data=MainMenu.cancel_vacation_menu.name,
        text=buttons.main_menu.CANCEL_VACATION_MENU
    )
