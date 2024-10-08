import logging

from bot.event import Event

from src.buttons.reschedule_vacation import RescheduleVacationButtons as Buttons
from src.callbacks.reschedule_vacation.bot_button_callbacks import (confirm_vacation_selection_cb,
                                                                    enter_new_vacation_dates_cb,
                                                                    confirm_vacation_reschedule_cb)
from src.callbacks.common_bot_button import back_to_main_menu_cb
from src.callbacks.dispatchers import callback_dispatcher

logger = logging.getLogger(__name__)

annual_vacation_callbacks = {
    Buttons.CONFIRM_VACATION_SELECTION.callback_data: confirm_vacation_selection_cb,
    Buttons.ENTER_NEW_VACATION_DATES.callback_data: enter_new_vacation_dates_cb,
    Buttons.CONFIRM_VACATION_RESCHEDULE.callback_data: confirm_vacation_reschedule_cb,
    Buttons.BACK_TO_MAIN_MENU: back_to_main_menu_cb
}


# TODO: Rename function. It should be noted that this is only for bot buttons.
def reschedule_vacation_callback_dispatcher(bot, event: Event) -> None:
    callback_dispatcher(bot=bot, event=event, callbacks=annual_vacation_callbacks)
