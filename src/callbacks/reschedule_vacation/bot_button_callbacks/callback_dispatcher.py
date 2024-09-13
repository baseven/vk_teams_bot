import logging

from bot.event import Event

from src.actions import RescheduleVacationActions as Actions
from src.callbacks.reschedule_vacation.bot_button_callbacks import (select_vacation_to_reschedule_cb, create_vacation, confirm_reschedule_vacation_cb)
from src.callbacks.common_bot_button import back_to_main_menu_cb
from src.callbacks.callback_dispatcher import callback_dispatcher

logger = logging.getLogger(__name__)

annual_vacation_callbacks = {
    Actions.SELECT_VACATION_TO_RESCHEDULE.value: select_vacation_to_reschedule_cb,
    Actions.RESCHEDULE_VACATION.value: create_vacation,
    Actions.CONFIRM_VACATION_RESCHEDULE.value: confirm_reschedule_vacation_cb,
    Actions.BACK_TO_MAIN_MENU: back_to_main_menu_cb
}


# TODO: Rename function. It should be noted that this is only for bot buttons.
def reschedule_vacation_callback_dispatcher(bot, event: Event) -> None:
    callback_dispatcher(bot=bot, event=event, callbacks=annual_vacation_callbacks)
