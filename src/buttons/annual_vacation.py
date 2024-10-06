from src.buttons.bot_button import BotButton
from src.states.annual_vacation import AnnualVacation
from texts.buttons import buttons

#TODO: Replace back_to_main_menu with dynamic value
class AnnualVacationButtons:
    HANDLE_ANNUAL_VACATION = BotButton(
        callback_data=AnnualVacation.handle_annual_vacation.name,
        text=buttons.annual_vacation.HANDLE_ANNUAL_VACATION
    )
    CREATE_ANNUAL_VACATION = BotButton(
        callback_data=AnnualVacation.create_annual_vacation.name,
        text=buttons.annual_vacation.CREATE_ANNUAL_VACATION
    )
    CONFIRM_ANNUAL_VACATION = BotButton(
        callback_data=AnnualVacation.confirm_annual_vacation.name,
        text=buttons.annual_vacation.CONFIRM_ANNUAL_VACATION
    )
    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text=buttons.annual_vacation.BACK_TO_MAIN_MENU
    )
