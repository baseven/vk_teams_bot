from src.actions.bot_action import BotAction
from src.states.cancel_vacation import CancelVacation

class CancelVacationActions:
    """Действия, соответствующие кнопкам главного меню."""

    SELECT_VACATION_TO_CANCEL = BotAction(
        callback_data=CancelVacation.select_vacation_to_cancel.name,
        text=""
    )
    CONFIRM_VACATION_CANCELLATION = BotAction(
        callback_data=CancelVacation.confirm_vacation_cancellation.name,
        text="Удалить"
    )
    BACK_TO_MAIN_MENU = BotAction(
        callback_data="back_to_main_menu",
        text="Вернуться в главное меню"
    )
