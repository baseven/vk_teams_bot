from bot.event import Event

from callbacks.unpaid_vacation.bot_button.handle_vacation_cb import handle_unpaid_vacation
from src.callbacks.callback_dispatcher import callback_dispatcher
from src.callbacks.main_menu.bot_button import annual_vacation_menu_cb
from src.handlers.limits_and_schedule import handle_view_limits_and_schedule
from src.handlers.reschedule_vacation import handle_reschedule_vacation
from src.handlers.cancel_vacation import handle_cancel_vacation

main_menu_callbacks = {
    "annual_vacation_menu": annual_vacation_menu_cb,
    "unpaid_vacation": handle_unpaid_vacation,
    "view_limits_and_schedule": handle_view_limits_and_schedule,
    "reschedule_vacation": handle_reschedule_vacation,
    "cancel_vacation": handle_cancel_vacation,
}


def main_menu_callback_dispatcher(bot, event: Event) -> None:
    """Главный обработчик для команд основного меню.

    Args:
        bot: Экземпляр бота.
        event (Event): Данные события.
    """
    callback_dispatcher(bot=bot, event=event, callbacks=main_menu_callbacks)
