from bot.event import Event

from src.actions.annual_vacation import AnnualVacationActions
from src.actions.reschedule_vacation import RescheduleVacationActions
from src.callbacks.dispatchers import message_dispatcher
from src.callbacks.annual_vacation.message_callbacks import annual_vacation_message_cb
from src.callbacks.reschedule_vacation.message_callbacks import reschedule_vacation_message_cb

message_callbacks = {
    AnnualVacationActions.CREATE_ANNUAL_VACATION.callback_data: annual_vacation_message_cb,
    RescheduleVacationActions.ENTER_NEW_VACATION_DATES.callback_data: reschedule_vacation_message_cb,
}

def handle_incoming_message(bot, event: Event):
    """Main dispatcher for all incoming messages."""
    message_dispatcher(bot=bot, event=event, message_callbacks=message_callbacks)
