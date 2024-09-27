from src.actions.bot_action import BotAction
from src.states.annual_vacation import AnnualVacation

class AnnualVacationActions:
    """Действия, соответствующие кнопкам главного меню."""

    HANDLE_ANNUAL_VACATION = BotAction(
        callback_data=AnnualVacation.handle_annual_vacation.name,
        text=""
    )
    CREATE_ANNUAL_VACATION = BotAction(
        callback_data=AnnualVacation.create_annual_vacation.name,
        text="Другие даты"
    )
    CONFIRM_ANNUAL_VACATION = BotAction(
        callback_data=AnnualVacation.confirm_annual_vacation.name,
        text="Оформить"
    )
    BACK_TO_MAIN_MENU = BotAction(
        callback_data="back_to_main_menu",
        text="Вернуться в главное меню"
    )
