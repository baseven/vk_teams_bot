from src.buttons.bot_button import BotButton
from src.states.reschedule_vacation import RescheduleVacation

class RescheduleVacationButtons:
    """Buttons corresponding to the Reschedule Vacation buttons."""

    CONFIRM_VACATION_SELECTION = BotButton(
        callback_data=RescheduleVacation.confirm_vacation_selection.name,
        text=""
    )
    ENTER_NEW_VACATION_DATES = BotButton(
        callback_data=RescheduleVacation.enter_new_vacation_dates.name,
        text="Да,я хочу перенести этот отпуск"
    )
    CONFIRM_VACATION_RESCHEDULE = BotButton(
        callback_data=RescheduleVacation.confirm_vacation_reschedule.name,
        text="Оформить"
    )
    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text="Вернуться в главное меню"
    )
