from src.buttons.bot_button import BotButton
from texts.buttons import buttons

#TODO: Replace back_to_main_menu with dynamic value
class LimitsAndVacationsButtons:
    """Buttons corresponding to the Limits and Vacations buttons."""

    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text=buttons.limits_and_vacations.BACK_TO_MAIN_MENU
    )
