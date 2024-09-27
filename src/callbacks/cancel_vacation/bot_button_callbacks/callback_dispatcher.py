import logging

from bot.event import Event

from src.actions.cancel_vacation import CancelVacationActions as Actions
from src.callbacks.cancel_vacation.bot_button_callbacks import (confirm_vacation_cancellation_cb,
                                                                select_vacation_to_cancel_cb)
from src.callbacks.dispatchers import callback_dispatcher

logger = logging.getLogger(__name__)

cancel_vacation_callbacks = {
    Actions.SELECT_VACATION_TO_CANCEL.callback_data: select_vacation_to_cancel_cb,
    Actions.CONFIRM_VACATION_CANCELLATION.callback_data: confirm_vacation_cancellation_cb
}


def cancel_vacation_callback_dispatcher(bot, event: Event) -> None:
    callback_dispatcher(bot=bot, event=event, callbacks=cancel_vacation_callbacks)
