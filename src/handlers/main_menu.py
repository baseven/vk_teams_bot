import json
from bot.event import Event  # Импорт Event для типизации
from src.keyboards import main_menu_keyboard
from src.states import UserStateManager
from src.handlers.annual_vacation import annual_vacation_menu_cb
from src.handlers.limits_and_schedule import handle_view_limits_and_schedule
from src.handlers.reschedule_vacation import handle_reschedule_vacation
from src.handlers.cancel_vacation import handle_cancel_vacation


def handle_vacation_action(bot, state_machine, user_id: str, event: Event, message: str) -> None:
    """Обрабатывает действия, связанные с отпуском.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
        message (str): Сообщение для ответа пользователю.
    """
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=message,
        show_alert=False
    )
    state_machine.save_state()
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Меню отпусков: Выберите действие",
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
    )


def handle_unpaid_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает действия по оформлению отпуска без оплаты.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
    """
    handle_vacation_action(bot, state_machine, user_id, event, "Отпуск без оплаты оформлен")


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
    user_id = event.from_chat
    user_state = UserStateManager.get_state(user_id)
    callback_data = event.data.get('callbackData')
    callback = main_menu_callbacks.get(callback_data)
    if callback:
        callback(bot, user_state, user_id, event)
