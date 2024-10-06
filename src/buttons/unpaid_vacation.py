from src.buttons.bot_button import BotButton
from texts.buttons import buttons

#TODO: Replace back_to_main_menu with dynamic value
class UnpaidVacationButtons:
    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text=buttons.unpaid_vacation.BACK_TO_MAIN_MENU
    )
