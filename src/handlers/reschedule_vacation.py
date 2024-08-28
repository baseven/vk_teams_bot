import json
import logging
from bot.event import EventType
from src.keyboards import (main_menu_keyboard, reschedule_vacation_buttons, reschedule_vacation_keyboard,
                           reschedule_accept_period_keyboard
                           )
from src.states.state_machine import BotStateMachine
from src.data.vacation_limits import vacation_limits
from src.data.vacation_schedule import vacation_schedule

logger = logging.getLogger(__name__)

PLANNED_VACATION_CALLBACK = "change_planned_vacation"
PRIMARY_STYLE = "primary"
PLANNED_VACATION_TEXT_TEMPLATE = (
    "Вывожу запланированные отпуска. Можете выбрать один из них для редактирования. "
    "Доступно дней для оформления отпуска: {available_days}, но можно оформить и другое количество."
)


def create_vacation_buttons(planned_vacations):
    """Создает кнопки для плановых отпусков."""
    return [
        [{
            "text": f"{vacation['start_date']} - {vacation['end_date']}",
            "callbackData": f"{PLANNED_VACATION_CALLBACK}_{vacation['start_date']} - {vacation['end_date']}",
            "style": PRIMARY_STYLE
        }]
        for vacation in planned_vacations
    ]


def handle_reschedule_vacation(bot, state_machine, user_id, event):
    logger.info(f"Starting annual vacation process for user {user_id}")
    state_machine.to_reschedule_vacation_menu()
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    # Здесь будет запрос к БД для получения доступных плановых периодов
    # Создание кнопок для плановых отпусков
    planned_vacations_buttons = create_vacation_buttons(vacation_schedule)
    reschedule_vacation_menu_keyboard = planned_vacations_buttons + reschedule_vacation_buttons

    # Здесь будет запрос к БД для получения доступных дней
    annual_vacation_text = PLANNED_VACATION_TEXT_TEMPLATE.format(available_days=vacation_limits.get("annual", 0))

    # Обновление сообщения с кнопками
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=annual_vacation_text,
        inline_keyboard_markup=json.dumps(reschedule_vacation_menu_keyboard)
    )


confirm_period_TEXT_TEMPLATE = "изменить отпуск {period}?"


def handle_change_planned_vacation(bot, state_machine, user_id, event, vacation_dates):
    logger.info(f" handle_planned_vacation for user {user_id}")
    state_machine.to_reschedule_vacation_change_period()
    state_machine.set_vacation_dates(vacation_dates)
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    confirm_period_text = confirm_period_TEXT_TEMPLATE.format(period=vacation_dates)
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=confirm_period_text,
        inline_keyboard_markup=json.dumps(reschedule_vacation_keyboard)
    )


def handle_change_vacation(bot, state_machine, user_id, event):
    logger.info(f" handle_change_vacation for user {user_id}")
    state_machine.to_reschedule_vacation_create_vacation()
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    create_vacation_text = "Введите период. Пожалуйста, укажите период в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ"

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=create_vacation_text
    )


def handle_confirm_change_vacation(bot, state_machine, user_id, event):
    logger.info(f" handle_confirm_vacation for user {user_id}")
    state_machine.to_main_menu()
    vacation_dates = state_machine.get_vacation_dates()
    state_machine.reset_vacation_dates()
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

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
        inline_keyboard_markup=main_menu_keyboard
    )


reschedule_vacation_cb_handlers = {
    PLANNED_VACATION_CALLBACK: handle_change_planned_vacation,
    "confirm_change_vacation": handle_confirm_change_vacation
}


def handle_reschedule_vacation_message(bot, state_machine, user_id, event):
    logger.info(f" handle_accept_vacation for user {user_id}")

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


def reschedule_vacation_message_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    logger.info(f"reschedule_vacation_message_cb for user: {user_id}, state: {state_machine.state}")
    if state_machine.state != "reschedule_vacation_create_vacation":
        logger.info(
            f"reschedule_vacation_message_cb: state {state_machine.state} != reschedule_vacation_create_vacation")
        return
    logger.info(f"event.type == {event.type}")
    if event.type == EventType.NEW_MESSAGE:
        logger.info(f"reschedule_vacation_message_cb: event.type == EventType.NEW_MESSAGE")
        handle_reschedule_vacation_message(bot, state_machine, user_id, event)


def reschedule_vacation_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data.get('callbackData')
    # Проверка на префикс "planned_vacation"
    if callback_data.startswith(PLANNED_VACATION_CALLBACK):
        # Извлечение даты отпуска из callbackData
        vacation_dates = callback_data[len(PLANNED_VACATION_CALLBACK) + 1:]  # +1 для учета "_"
        handler = handle_change_planned_vacation

        if handler:
            handler(bot, state_machine, user_id, event, vacation_dates)
    else:
        handler = reschedule_vacation_cb_handlers.get(callback_data)
        if handler:
            handler(bot, state_machine, user_id, event)
