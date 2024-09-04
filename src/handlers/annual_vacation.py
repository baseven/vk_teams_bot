import json
import logging
from bot.event import Event, EventType
from src.keyboards import (annual_vacation_buttons, confirm_period_keyboard,
                           main_menu_keyboard, accept_period_keyboard)
from src.states.state_machine import BotStateMachine
from src.models.vacation import Vacation, VacationType, VacationStatus
from src.data.vacation_limits import vacation_limits_dict
from src.data.vacation_schedule import vacation_schedule
from src.utils import create_vacation_buttons  # Импортируем функцию из utils.py

# Настройка логгера для модуля
logger = logging.getLogger(__name__)

# Константы
PLANNED_VACATION_CALLBACK = "planned_vacation"
PRIMARY_STYLE = "primary"
ANNUAL_VACATION_TEXT_TEMPLATE = (
    "Вывожу доступные плановые периоды. Можете выбрать один из них или выбрать другие даты. "
    "Доступно дней для оформления отпуска: {available_days}, но можно оформить и другое количество."
)
CONFIRM_PERIOD_TEXT_TEMPLATE = "Оформить отпуск на {period} или вы хотите немного изменить даты?"


def handle_annual_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    logger.info(f"Starting annual vacation process for user {user_id}")

    state_machine.to_annual_vacation_menu()
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    # Используем общую функцию для создания кнопок
    planned_vacations_buttons = create_vacation_buttons(
        planned_vacations=vacation_schedule,
        callback_prefix=PLANNED_VACATION_CALLBACK,
        button_style=PRIMARY_STYLE
    )

    annual_vacation_menu_keyboard = planned_vacations_buttons + annual_vacation_buttons
    available_days = vacation_limits_dict[VacationType.ANNUAL_PAID].available_days
    annual_vacation_text = ANNUAL_VACATION_TEXT_TEMPLATE.format(available_days=available_days)

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=annual_vacation_text,
        inline_keyboard_markup=json.dumps(annual_vacation_menu_keyboard)
    )


def handle_planned_vacation(bot, state_machine, user_id: str, event: Event,
                            vacation_dates: str) -> None:
    """Обрабатывает выбор планового отпуска пользователем."""
    logger.info(f"Handling planned vacation for user {user_id}")

    state_machine.to_annual_vacation_confirm_period()
    state_machine.set_vacation_dates(vacation_dates)
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    confirm_period_text = CONFIRM_PERIOD_TEXT_TEMPLATE.format(period=vacation_dates)
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=confirm_period_text,
        inline_keyboard_markup=json.dumps(confirm_period_keyboard)
    )


def handle_confirm_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает подтверждение оформления отпуска пользователем."""
    logger.info(f"Handling confirm vacation for user {user_id}")

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


def handle_create_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает создание нового отпуска пользователем."""
    logger.info(f"Handling create new vacation for user {user_id}")

    state_machine.to_annual_vacation_create_vacation()
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    create_vacation_text = "Введите период. Пожалуйста, укажите период в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ"

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=create_vacation_text
    )


def handle_accept_vacation(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает подтверждение пользователем оформления нового отпуска."""
    logger.info(f"Handling accept vacation for user {user_id}")

    vacation_dates = event.data['text']
    state_machine.set_vacation_dates(vacation_dates)
    state_machine.save_state()
    accept_vacation_text = f"Вы точно хотите оформить отпуск на {vacation_dates}?"

    bot.delete_messages(chat_id=user_id, msg_id=state_machine.last_message_id)
    response = bot.send_text(
        chat_id=user_id,
        text=accept_vacation_text,
        inline_keyboard_markup=json.dumps(accept_period_keyboard)
    )
    logger.info(f"Response: {response.json()}")
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()


def handle_back_to_main_menu(bot, state_machine, user_id: str, event: Event) -> None:
    """Возвращает пользователя в главное меню."""
    logger.info(f"Handling back to main menu for user {user_id}")

    state_machine.to_main_menu()
    state_machine.reset_vacation_dates()
    state_machine.save_state()
    logger.info(f"State saved: {state_machine.state}")

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Главное меню",
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
    )


annual_vacation_cb_handlers = {
    PLANNED_VACATION_CALLBACK: handle_planned_vacation,
    "confirm_planned_vacation": handle_confirm_vacation,
    "create_new_vacation": handle_create_vacation,
    "back_to_main_menu": handle_back_to_main_menu
}


def annual_vacation_message_cb(bot, event: Event) -> None:
    """Обрабатывает входящие сообщения, связанные с ежегодными отпусками."""
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    logger.info(f"annual_vacation_message_cb for user: {user_id}, state: {state_machine.state}")

    if state_machine.state != "annual_vacation_create_vacation":
        logger.info(f"State mismatch: {state_machine.state} != annual_vacation_create_vacation")
        return

    logger.info(f"Event type: {event.type}")
    if event.type == EventType.NEW_MESSAGE:
        logger.info(f"Handling new message event for user {user_id}")
        handle_accept_vacation(bot, state_machine, user_id, event)


def annual_vacation_cb(bot, event: Event) -> None:
    """Обрабатывает обратные вызовы, связанные с ежегодными отпусками."""
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data.get('callbackData')

    if callback_data.startswith(PLANNED_VACATION_CALLBACK):
        vacation_dates = callback_data[len(PLANNED_VACATION_CALLBACK) + 1:]  # +1 для учета "_"
        handler = handle_planned_vacation

        if handler:
            handler(bot, state_machine, user_id, event, vacation_dates)
    else:
        handler = annual_vacation_cb_handlers.get(callback_data)
        if handler:
            handler(bot, state_machine, user_id, event)
