import logging

from bot.event import Event

from src.actions import AnnualVacationActions as Actions
from src.callbacks.annual_vacation.bot_button_callbacks import (confirm_annual_vacation_cb, create_annual_vacation_cb,
                                                                handle_annual_vacation_cb)
from src.callbacks.common_bot_button import back_to_main_menu_cb
from src.callbacks.callback_dispatcher import callback_dispatcher

logger = logging.getLogger(__name__)

annual_vacation_callbacks = {
    Actions.HANDLE_ANNUAL_VACATION.value: handle_annual_vacation_cb,
    Actions.CREATE_ANNUAL_VACATION.value: create_annual_vacation_cb,
    Actions.CONFIRM_ANNUAL_VACATION.value: confirm_annual_vacation_cb,
    Actions.BACK_TO_MAIN_MENU: back_to_main_menu_cb
}


# TODO: Rename function. It should be noted that this is only for bot buttons.
def annual_vacation_callback_dispatcher(bot, event: Event) -> None:
    callback_dispatcher(bot=bot, event=event, callbacks=annual_vacation_callbacks)
