from bot.event import Event

from src.callbacks.dispatchers import message_dispatcher
from src.callbacks.annual_vacation.message_callbacks import annual_vacation_message_cb
from src.callbacks.reschedule_vacation.message_callbacks import reschedule_vacation_message_cb

message_callbacks = {
    'create_annual_vacation': annual_vacation_message_cb,
    'entering_new_vacation_dates': reschedule_vacation_message_cb,
}

def handle_incoming_message(bot, event: Event):
    """Main dispatcher for all incoming messages."""
    message_dispatcher(bot=bot, event=event, message_callbacks=message_callbacks)
