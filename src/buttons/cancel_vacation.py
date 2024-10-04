from src.buttons.bot_button import BotButton
from src.states.cancel_vacation import CancelVacation

class CancelVacationButtons:
    """Buttons corresponding to the Cancel Vacation buttons."""

    SELECT_VACATION_TO_CANCEL = BotButton(
        callback_data=CancelVacation.select_vacation_to_cancel.name,
        text=""
    )
    CONFIRM_VACATION_CANCELLATION = BotButton(
        callback_data=CancelVacation.confirm_vacation_cancellation.name,
        text="Удалить"
    )
    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text="Вернуться в главное меню"
    )
