from src.buttons.bot_button import BotButton
from src.states.annual_vacation import AnnualVacation

class AnnualVacationButtons:
    """Buttons corresponding to the Annual Vacation buttons."""

    HANDLE_ANNUAL_VACATION = BotButton(
        callback_data=AnnualVacation.handle_annual_vacation.name,
        text=""
    )
    CREATE_ANNUAL_VACATION = BotButton(
        callback_data=AnnualVacation.create_annual_vacation.name,
        text="Другие даты"
    )
    CONFIRM_ANNUAL_VACATION = BotButton(
        callback_data=AnnualVacation.confirm_annual_vacation.name,
        text="Оформить"
    )
    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text="Вернуться в главное меню"
    )
