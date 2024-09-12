from bot.handler import BotButtonCommandHandler, StartCommandHandler, MessageHandler

from src.callbacks import (
    start_cb,
    main_menu_callback_dispatcher,
    annual_vacation_callback_dispatcher,
    annual_vacation_message_cb,

)

# Словарь обработчиков: ключ - класс обработчика, значение - список callback-функций
HANDLERS = {
    StartCommandHandler: [start_cb],
    BotButtonCommandHandler: [
        main_menu_callback_dispatcher,
        annual_vacation_callback_dispatcher,
    ],
    MessageHandler: [annual_vacation_message_cb]
}


def register_handlers(bot) -> None:
    """Регистрирует все команды и кнопочные обработчики для бота.

    Args:
        bot: Экземпляр бота.
    """
    for handler_class, callbacks in HANDLERS.items():
        for callback in callbacks:
            bot.dispatcher.add_handler(handler_class(callback=callback))
