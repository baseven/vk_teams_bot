import json
import logging
from bot.event import EventType
from src.keyboards import (main_menu_keyboard, cancel_vacation_buttons, cancel_vacation_keyboard,
                           reschedule_accept_period_keyboard
                           )
from src.states.state_machine import BotStateMachine
from src.data.vacation_limits import vacation_limits
from src.data.vacation_schedule import vacation_schedule

logger = logging.getLogger(__name__)

PLANNED_VACATION_CALLBACK = "cancel_planned_vacation"
PRIMARY_STYLE = "primary"
PLANNED_VACATION_TEXT_TEMPLATE = "Вывожу запланированные отпуска. Можете выбрать один из них для удаления."


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


def handle_cancel_vacation(bot, state_machine, user_id, event):
    logger.info(f"Starting handle_cancel_vacation process for user {user_id}")
    state_machine.to_cancel_vacation_menu()
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    # Здесь будет запрос к БД для получения доступных плановых периодов
    # Создание кнопок для плановых отпусков
    planned_vacations_buttons = create_vacation_buttons(vacation_schedule)
    cancel_vacation_menu_keyboard = planned_vacations_buttons + cancel_vacation_buttons

    # Обновление сообщения с кнопками
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=PLANNED_VACATION_TEXT_TEMPLATE,
        inline_keyboard_markup=json.dumps(cancel_vacation_menu_keyboard)
    )


confirm_cancel_period_TEXT_TEMPLATE = "Удалить отпуск {period}?"


def handle_cancel_planned_vacation(bot, state_machine, user_id, event, vacation_dates):
    logger.info(f" handle_planned_vacation for user {user_id}")
    state_machine.to_cancel_vacation_delete_period()
    state_machine.set_vacation_dates(vacation_dates)
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    confirm_period_text = confirm_cancel_period_TEXT_TEMPLATE.format(period=vacation_dates)
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=confirm_period_text,
        inline_keyboard_markup=json.dumps(cancel_vacation_keyboard)
    )


def handle_confirm_cancel_vacation(bot, state_machine, user_id, event):
    logger.info(f" handle_confirm_cancel_vacation for user {user_id}")
    state_machine.to_main_menu()
    vacation_dates = state_machine.get_vacation_dates()
    state_machine.reset_vacation_dates()
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    confirm_vacation_text = f"Eжегоднsq отпуск {vacation_dates} удален"
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


cancel_vacation_cb_handlers = {
    PLANNED_VACATION_CALLBACK: handle_cancel_planned_vacation,
    "confirm_cancel_vacation": handle_confirm_cancel_vacation
}


def cancel_vacation_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data.get('callbackData')
    # Проверка на префикс "planned_vacation"
    if callback_data.startswith(PLANNED_VACATION_CALLBACK):
        # Извлечение даты отпуска из callbackData
        vacation_dates = callback_data[len(PLANNED_VACATION_CALLBACK) + 1:]  # +1 для учета "_"
        handler = handle_cancel_planned_vacation

        if handler:
            handler(bot, state_machine, user_id, event, vacation_dates)
    else:
        handler = cancel_vacation_cb_handlers.get(callback_data)
        if handler:
            handler(bot, state_machine, user_id, event)
