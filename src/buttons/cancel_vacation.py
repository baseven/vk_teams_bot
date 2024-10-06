from src.buttons.bot_button import BotButton
from src.states.cancel_vacation import CancelVacation
from texts.buttons import buttons

#TODO: Replace back_to_main_menu with dynamic value
class CancelVacationButtons:
    SELECT_VACATION_TO_CANCEL = BotButton(
        callback_data=CancelVacation.select_vacation_to_cancel.name,
        text=buttons.cancel_vacation.SELECT_VACATION_TO_CANCEL
    )
    CONFIRM_VACATION_CANCELLATION = BotButton(
        callback_data=CancelVacation.confirm_vacation_cancellation.name,
        text=buttons.cancel_vacation.CONFIRM_VACATION_CANCELLATION
    )
    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text=buttons.cancel_vacation.BACK_TO_MAIN_MENU
    )
