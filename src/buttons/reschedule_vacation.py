from src.buttons.bot_button import BotButton
from src.states.reschedule_vacation import RescheduleVacation
from texts.buttons import buttons

#TODO: Replace back_to_main_menu with dynamic value
class RescheduleVacationButtons:
    CONFIRM_VACATION_SELECTION = BotButton(
        callback_data=RescheduleVacation.confirm_vacation_selection.name,
        text=buttons.reschedule_vacation.CONFIRM_VACATION_SELECTION
    )
    ENTER_NEW_VACATION_DATES = BotButton(
        callback_data=RescheduleVacation.enter_new_vacation_dates.name,
        text=buttons.reschedule_vacation.ENTER_NEW_VACATION_DATES
    )
    CONFIRM_VACATION_RESCHEDULE = BotButton(
        callback_data=RescheduleVacation.confirm_vacation_reschedule.name,
        text=buttons.reschedule_vacation.CONFIRM_VACATION_RESCHEDULE
    )
    BACK_TO_MAIN_MENU = BotButton(
        callback_data="back_to_main_menu",
        text=buttons.reschedule_vacation.BACK_TO_MAIN_MENU
    )
