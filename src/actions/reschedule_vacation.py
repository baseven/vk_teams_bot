from src.actions.bot_action import BotAction
from src.states.reschedule_vacation import RescheduleVacation

class RescheduleVacationActions:
    """Действия, соответствующие кнопкам главного меню."""
    CONFIRM_VACATION_SELECTION = BotAction(
        callback_data=RescheduleVacation.confirm_vacation_selection.name,
        text=""
    )
    ENTER_NEW_VACATION_DATES = BotAction(
        callback_data=RescheduleVacation.enter_new_vacation_dates.name,
        text="Да,я хочу перенести этот отпуск"
    )
    CONFIRM_VACATION_RESCHEDULE = BotAction(
        callback_data=RescheduleVacation.confirm_vacation_reschedule.name,
        text="Оформить"
    )
    BACK_TO_MAIN_MENU = BotAction(
        callback_data="back_to_main_menu",
        text="Вернуться в главное меню"
    )
