from src.buttons.bot_button import BotButton

class LimitsAndVacationsButtons:
    """Buttons corresponding to the Limits and Vacations buttons."""

    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text="Вернуться в главное меню"
    )
