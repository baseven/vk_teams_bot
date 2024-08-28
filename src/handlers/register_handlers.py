from bot.handler import BotButtonCommandHandler, StartCommandHandler, MessageHandler

from src.handlers import (
    start_cb,
    main_menu_cb,
    annual_vacation_cb,
    annual_vacation_message_cb,
    reschedule_vacation_cb,
    cancel_vacation_cb
)

# Dictionary of handlers: key is the handler class, value is a list of callback functions
HANDLERS = {
    StartCommandHandler: [start_cb],
    BotButtonCommandHandler: [
        main_menu_cb,
        annual_vacation_cb,
        reschedule_vacation_cb,
        cancel_vacation_cb
    ],
    MessageHandler: [annual_vacation_message_cb]
}


def register_handlers(bot):
    """Register all command and button handlers for the bot."""
    for handler_class, callbacks in HANDLERS.items():
        for callback in callbacks:
            bot.dispatcher.add_handler(handler_class(callback=callback))
