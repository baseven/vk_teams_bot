import logging

from bot.event import Event

from src.buttons.annual_vacation import AnnualVacationButtons as Buttons
from src.callbacks.annual_vacation.bot_button_callbacks import (confirm_annual_vacation_cb, create_annual_vacation_cb,
                                                                handle_annual_vacation_cb)
from src.callbacks.common_bot_button import back_to_main_menu_cb
from src.callbacks.dispatchers import callback_dispatcher

logger = logging.getLogger(__name__)

annual_vacation_callbacks = {
    Buttons.HANDLE_ANNUAL_VACATION.callback_data: handle_annual_vacation_cb,
    Buttons.CREATE_ANNUAL_VACATION.callback_data: create_annual_vacation_cb,
    Buttons.CONFIRM_ANNUAL_VACATION.callback_data: confirm_annual_vacation_cb,
    Buttons.BACK_TO_MAIN_MENU.callback_data: back_to_main_menu_cb
}


# TODO: Rename function. It should be noted that this is only for bot buttons.
def annual_vacation_callback_dispatcher(bot, event: Event) -> None:
    callback_dispatcher(bot=bot, event=event, callbacks=annual_vacation_callbacks)
