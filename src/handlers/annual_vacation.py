import json
import logging
from bot.event import EventType
from src.keyboards import annual_vacation_buttons, confirm_period_keyboard, main_menu_keyboard, accept_period_keyboard
from src.states.state_machine import BotStateMachine

# Настройка логгера для модуля
logger = logging.getLogger(__name__)

# Константы
PLANNED_VACATION_CALLBACK = "planned_vacation"
PRIMARY_STYLE = "primary"
ANNUAL_VACATION_TEXT_TEMPLATE = (
    "Вывожу доступные плановые периоды. Можете выбрать один из них или выбрать другие даты. "
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


def handle_annual_vacation(bot, state_machine, user_id, event):
    logger.info(f"Starting annual vacation process for user {user_id}")
    state_machine.to_annual_vacation_menu()
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    # Здесь будет запрос к БД для получения доступных плановых периодов
    planned_vacations = [
        {"start_date": "01.01.2025", "end_date": "10.01.2025"},
        {"start_date": "01.02.2025", "end_date": "10.02.2025"}
    ]

    # Создание кнопок для плановых отпусков
    planned_vacations_buttons = create_vacation_buttons(planned_vacations)
    annual_vacation_menu_keyboard = planned_vacations_buttons + annual_vacation_buttons

    # Здесь будет запрос к БД для получения доступных дней
    available_days = 21
    annual_vacation_text = ANNUAL_VACATION_TEXT_TEMPLATE.format(available_days=available_days)

    # Обновление сообщения с кнопками
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=annual_vacation_text,
        inline_keyboard_markup=json.dumps(annual_vacation_menu_keyboard)
    )


confirm_period_TEXT_TEMPLATE = "Оформить отпуск на {period} или вы хотите немного изменить даты?"


def handle_planned_vacation(bot, state_machine, user_id, event, vacation_dates):
    logger.info(f" handle_planned_vacation for user {user_id}")
    state_machine.to_annual_vacation_confirm_period()
    state_machine.set_vacation_dates(vacation_dates)
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    confirm_period_text = confirm_period_TEXT_TEMPLATE.format(period=vacation_dates)
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=confirm_period_text,
        inline_keyboard_markup=json.dumps(confirm_period_keyboard)
    )


def handle_confirm_vacation(bot, state_machine, user_id, event):
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


def handle_create_vacation(bot, state_machine, user_id, event):
    logger.info(f" handle_create_new_vacation for user {user_id}")
    state_machine.to_annual_vacation_create_vacation()
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    create_vacation_text = "Введите период. Пожалуйста, укажите период в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ"

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=create_vacation_text
    )


def handle_accept_vacation(bot, state_machine, user_id, event):
    logger.info(f" handle_accept_vacation for user {user_id}")

    vacation_dates = event.data['text']
    state_machine.set_vacation_dates(vacation_dates)
    state_machine.save_state()
    accept_vacation_text = f"Вы точно хотите оформить отпуск на {vacation_dates}?"

    # bot.edit_text(
    #     chat_id=user_id,
    #     msg_id=state_machine.last_message_id,
    #     text=accept_vacation_text,
    #     inline_keyboard_markup=json.dumps(accept_period_keyboard)
    # )

    bot.delete_messages(chat_id=user_id, msg_id=state_machine.last_message_id)
    response = bot.send_text(
        chat_id=user_id,
        text=accept_vacation_text,
        inline_keyboard_markup=json.dumps(accept_period_keyboard)
    )
    logger.info(f"Response: {response.json()}")
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()


def handle_back_to_main_menu(bot, state_machine, user_id, event):
    logger.info(f" handle_back_to_main_menu for user {user_id}")
    state_machine.to_main_menu()
    state_machine.reset_vacation_dates()  # TODO: Точно ли нужен?
    state_machine.save_state()
    logger.info(f"Saving state {state_machine.state}")

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Главное меню",
        inline_keyboard_markup=main_menu_keyboard
    )


# TODO: There is a relationship with callbackData in vacations_menu_buttons. This needs to be refactored.
annual_vacation_cb_handlers = {
    PLANNED_VACATION_CALLBACK: handle_planned_vacation,
    "confirm_planned_vacation": handle_confirm_vacation,
    "create_new_vacation": handle_create_vacation,
    "back_to_main_menu": handle_back_to_main_menu
}


def annual_vacation_message_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    logger.info(f"annual_vacation_message_cb for user: {user_id}, state: {state_machine.state}")
    if state_machine.state != "annual_vacation_create_vacation":
        logger.info(f"annual_vacation_message_cb: state {state_machine.state} != annual_vacation_create_vacation")
        return
    logger.info(f"event.type == {event.type}")
    if event.type == EventType.NEW_MESSAGE:
        logger.info(f"annual_vacation_message_cb: event.type == EventType.NEW_MESSAGE")
        handle_accept_vacation(bot, state_machine, user_id, event)

    # TODO: Add event type checking


def annual_vacation_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data.get('callbackData')
    # Проверка на префикс "planned_vacation"
    if callback_data.startswith(PLANNED_VACATION_CALLBACK):
        # Извлечение даты отпуска из callbackData
        vacation_dates = callback_data[len(PLANNED_VACATION_CALLBACK) + 1:]  # +1 для учета "_"
        handler = handle_planned_vacation

        if handler:
            handler(bot, state_machine, user_id, event, vacation_dates)
    else:
        handler = annual_vacation_cb_handlers.get(callback_data)
        if handler:
            handler(bot, state_machine, user_id, event)
