from src.buttons.bot_button import BotButton

class UnpaidVacationButtons:
    """Buttons corresponding to the Unpaid Vacation buttons."""

    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text="Вернуться в главное меню"
    )
