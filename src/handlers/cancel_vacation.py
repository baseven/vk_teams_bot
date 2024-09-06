import json
import logging
from typing import List
from bot.event import Event, EventType  # Импорт Event
from src.keyboards import (main_menu_keyboard, cancel_vacation_buttons,
                           cancel_vacation_keyboard, reschedule_accept_period_keyboard)
from src.states.state_machine import BotStateMachine
from src.models.vacation import Vacation
from src.data.vacation_schedule import vacation_schedule
from src.utils import create_vacation_buttons  # Импортируем функцию из utils.py

# Настройка логгера для модуля
logger = logging.getLogger(__name__)

# Константы
PLANNED_VACATION_CALLBACK = "cancel_planned_vacation"
PRIMARY_STYLE = "primary"
PLANNED_VACATION_TEXT_TEMPLATE = "Вывожу запланированные отпуска. Можете выбрать один из них для удаления."
CONFIRM_CANCEL_PERIOD_TEXT_TEMPLATE = "Удалить отпуск {period}?"


def handle_cancel_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает запрос на отмену отпуска.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
    """
    logger.info(f"Starting handle_cancel_vacation process for user {user_id}")

    state_machine.to_cancel_vacation_menu()
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    # Используем общую функцию для создания кнопок
    planned_vacations_buttons = create_vacation_buttons(
        planned_vacations=vacation_schedule,
        callback_prefix=PLANNED_VACATION_CALLBACK,
        button_style=PRIMARY_STYLE
    )

    cancel_vacation_menu_keyboard = planned_vacations_buttons + cancel_vacation_buttons

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=PLANNED_VACATION_TEXT_TEMPLATE,
        inline_keyboard_markup=json.dumps(cancel_vacation_menu_keyboard)
    )


def handle_cancel_planned_vacation(bot, state_machine, user_id: str, event: Event, vacation_dates: str) -> None:
    """Обрабатывает выбор пользователем отпуска для отмены.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
        vacation_dates (str): Даты отпуска для отмены.
    """
    logger.info(f"Handling cancel planned vacation for user {user_id}")

    state_machine.to_cancel_vacation_delete_period()
    state_machine.set_vacation_dates(vacation_dates)
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    confirm_period_text = CONFIRM_CANCEL_PERIOD_TEXT_TEMPLATE.format(period=vacation_dates)
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=confirm_period_text,
        inline_keyboard_markup=json.dumps(cancel_vacation_keyboard)
    )


def handle_confirm_cancel_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает подтверждение отмены отпуска пользователем.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
    """
    logger.info(f"Handling confirm cancel vacation for user {user_id}")

    state_machine.to_main_menu()
    vacation_dates = state_machine.get_vacation_dates()
    state_machine.reset_vacation_dates()
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    confirm_vacation_text = f"Ежегодный отпуск {vacation_dates} удален"
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


cancel_vacation_cb_handlers = {
    PLANNED_VACATION_CALLBACK: handle_cancel_planned_vacation,
    "confirm_cancel_vacation": handle_confirm_cancel_vacation
}


def cancel_vacation_cb(bot, event: Event) -> None:
    """Обрабатывает обратные вызовы, связанные с отменой отпусков.

    Args:
        bot: Экземпляр бота.
        event (Event): Данные события.
    """
    user_id = event.from_chat
    state_machine = BotStateMachine.get_state(user_id)
    callback_data = event.data.get('callbackData')

    if callback_data.startswith(PLANNED_VACATION_CALLBACK):
        vacation_dates = callback_data[len(PLANNED_VACATION_CALLBACK) + 1:]  # +1 для учета "_"
        handler = handle_cancel_planned_vacation

        if handler:
            handler(bot, state_machine, user_id, event, vacation_dates)
    else:
        handler = cancel_vacation_cb_handlers.get(callback_data)
        if handler:
            handler(bot, state_machine, user_id, event)
