import json
import logging
from bot.event import Event, EventType  # Импорт Event и EventType для типизации
from src.keyboards import (main_menu_keyboard, reschedule_vacation_buttons,
                           reschedule_vacation_keyboard, reschedule_accept_period_keyboard)
from src.states.state_machine import UserStateMachine
from src.models.vacation import Vacation
from src.data.vacation_limits import vacation_limits
from src.data.vacation_schedule import vacation_schedule
from src.utils import create_vacation_buttons  # Импортируем функцию из utils.py

logger = logging.getLogger(__name__)

PLANNED_VACATION_CALLBACK = "change_planned_vacation"
PRIMARY_STYLE = "primary"
PLANNED_VACATION_TEXT_TEMPLATE = (
    "Вывожу запланированные отпуска. Можете выбрать один из них для редактирования. "
    "Доступно дней для оформления отпуска: {available_days}, но можно оформить и другое количество."
)


def handle_reschedule_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает запрос на перенос отпуска.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
    """
    logger.info(f"Starting reschedule vacation process for user {user_id}")

    state_machine.to_reschedule_vacation_menu()
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    # Используем общую функцию для создания кнопок
    planned_vacations_buttons = create_vacation_buttons(
        planned_vacations=vacation_schedule,
        callback_prefix=PLANNED_VACATION_CALLBACK,
        button_style=PRIMARY_STYLE
    )

    reschedule_vacation_menu_keyboard = planned_vacations_buttons + reschedule_vacation_buttons

    available_days = vacation_limits.get("annual", 0)
    reschedule_text = PLANNED_VACATION_TEXT_TEMPLATE.format(available_days=available_days)

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=reschedule_text,
        inline_keyboard_markup=json.dumps(reschedule_vacation_menu_keyboard)
    )


confirm_period_TEXT_TEMPLATE = "Изменить отпуск {period}?"


def handle_change_planned_vacation(bot, state_machine, user_id: str, event: Event, vacation_dates: str) -> None:
    """Обрабатывает изменение выбранного отпуска.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
        vacation_dates (str): Даты отпуска для изменения.
    """
    logger.info(f"Handling change planned vacation for user {user_id}")

    state_machine.to_reschedule_vacation_change_period()
    state_machine.set_vacation_dates(vacation_dates)
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    confirm_period_text = confirm_period_TEXT_TEMPLATE.format(period=vacation_dates)
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=confirm_period_text,
        inline_keyboard_markup=json.dumps(reschedule_vacation_keyboard)
    )


def handle_change_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает изменение отпуска.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
    """
    logger.info(f"Handling change vacation for user {user_id}")

    state_machine.to_reschedule_vacation_create_vacation()
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    create_vacation_text = "Введите период. Пожалуйста, укажите период в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ"

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=create_vacation_text
    )


def handle_confirm_change_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает подтверждение изменения отпуска.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
    """
    logger.info(f"Handling confirm change vacation for user {user_id}")

    state_machine.to_main_menu()
    vacation_dates = state_machine.get_vacation_dates()
    state_machine.reset_vacation_dates()
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    confirm_vacation_text = f"Оформление ежегодного отпуска {vacation_dates} отправлено на согласование"
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=confirm_vacation_text,
        show_alert=False
    )

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Главное меню",
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
    )


reschedule_vacation_cb_handlers = {
    PLANNED_VACATION_CALLBACK: handle_change_planned_vacation,
    "confirm_change_vacation": handle_confirm_change_vacation
}


def handle_reschedule_vacation_message(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает сообщение о переносе отпуска.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
    """
    logger.info(f"Handling reschedule vacation message for user {user_id}")

    vacation_dates = event.data['text']
    state_machine.set_vacation_dates(vacation_dates)
    state_machine.save_state()
    accept_vacation_text = f"Вы точно хотите оформить отпуск на {vacation_dates}?"

    bot.delete_messages(chat_id=user_id, msg_id=state_machine.last_message_id)
    response = bot.send_text(
        chat_id=user_id,
        text=accept_vacation_text,
        inline_keyboard_markup=json.dumps(reschedule_accept_period_keyboard)
    )
    logger.info(f"Response: {response.json()}")
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()


def reschedule_vacation_message_cb(bot, event: Event) -> None:
    """Обрабатывает обратные вызовы для сообщений о переносе отпуска.

    Args:
        bot: Экземпляр бота.
        event (Event): Данные события.
    """
    user_id = event.from_chat
    state_machine = UserStateMachine.get_state(user_id)
    logger.info(f"reschedule_vacation_message_cb for user: {user_id}, state: {state_machine.state}")

    if state_machine.state != "reschedule_vacation_create_vacation":
        logger.info(
            f"State mismatch: {state_machine.state} != reschedule_vacation_create_vacation"
        )
        return

    if event.type == EventType.NEW_MESSAGE:
        logger.info(f"Handling new message event for user {user_id}")
        handle_reschedule_vacation_message(bot, state_machine, user_id, event)


def reschedule_vacation_cb(bot, event: Event) -> None:
    """Обрабатывает обратные вызовы для переноса отпуска.

    Args:
        bot: Экземпляр бота.
        event (Event): Данные события.
    """
    user_id = event.from_chat
    state_machine = UserStateMachine.get_state(user_id)
    callback_data = event.data.get('callbackData')

    if callback_data.startswith(PLANNED_VACATION_CALLBACK):
        vacation_dates = callback_data[len(PLANNED_VACATION_CALLBACK) + 1:]  # +1 для учета "_"
        handler = handle_change_planned_vacation

        if handler:
            handler(bot, state_machine, user_id, event, vacation_dates)
    else:
        handler = reschedule_vacation_cb_handlers.get(callback_data)
        if handler:
            handler(bot, state_machine, user_id, event)
