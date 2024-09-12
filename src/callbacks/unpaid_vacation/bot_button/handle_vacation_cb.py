import json
from bot.event import Event

from keyboards import main_menu_keyboard


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