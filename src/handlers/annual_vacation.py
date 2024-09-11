import json
import logging
from bot.event import Event, EventType
from src.actions import AnnualVacationActions as Actions

from src.keyboards import (annual_vacation_buttons,
                           main_menu_keyboard, accept_period_keyboard)
from src.states import UserStateManager
from src.models.vacation import Vacation, VacationType, VacationStatus
from src.data.vacation_limits import vacation_limits_dict
from src.data.vacation_schedule import vacation_schedule
from src.utils import create_vacation_keyboard, create_keyboard, parse_callback_data, \
    parse_vacation_dates

logger = logging.getLogger(__name__)

ANNUAL_VACATION_MENU_TEXT_TEMPLATE = (
    "Вывожу доступные плановые периоды. Можете выбрать один из них или выбрать другие даты. "
    "Доступно дней для оформления отпуска: {available_days}, но можно оформить и другое количество."
)
HANDLE_ANNUAL_VACATION_TEXT_TEMPLATE = "Оформить отпуск на {period} или вы хотите немного изменить даты?"
CONFIRM_ANNUAL_VACATION_TEXT_TEMPLATE = "Оформление ежегодного отпуска {period} отправлено на согласование"
CREATE_ANNUAL_VACATION_TEXT = "Введите период. Пожалуйста, укажите период в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ"
HANDLE_ANNUAL_VACATION_DATES_TEXT_TEMPLATE = "Вы точно хотите оформить отпуск на {period}?"


def annual_vacation_menu_cb(
        bot,
        user_state: UserStateManager,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"Annual vacation menu callback for user {user_id}")

    user_state.state_machine.to_annual_vacation_menu()
    user_state.save_state()

    annual_vacation_keyboard = create_vacation_keyboard(
        planned_vacations=vacation_schedule,
        callback_prefix=Actions.HANDLE_ANNUAL_VACATION.value
    )

    actions = [
        Actions.CREATE_ANNUAL_VACATION,
        Actions.BACK_TO_MAIN_MENU
    ]
    annual_vacation_keyboard2 = create_keyboard(actions=actions)

    annual_vacation_menu_keyboard = annual_vacation_keyboard + annual_vacation_keyboard2
    available_days = vacation_limits_dict[VacationType.ANNUAL_PAID].available_days
    annual_vacation_text = ANNUAL_VACATION_MENU_TEXT_TEMPLATE.format(available_days=available_days)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_state.get_last_bot_message_id(),
        text=annual_vacation_text,
        inline_keyboard_markup=json.dumps(annual_vacation_menu_keyboard)
    )


def handle_annual_vacation_cb(
        bot,
        user_state: UserStateManager,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Handle annual vacation callback for {user_id}")

    user_state.state_machine.to_handle_annual_vacation()
    user_state.set_current_vacation(vacation_id=callback_data_value)
    user_state.save_state()

    start_date, end_date = user_state.get_current_vacation_dates()
    handle_annual_vacation_text = HANDLE_ANNUAL_VACATION_TEXT_TEMPLATE.format(period=f"{start_date}- {end_date}")

    actions = [
        Actions.CONFIRM_ANNUAL_VACATION,
        Actions.CREATE_ANNUAL_VACATION,
        Actions.BACK_TO_MAIN_MENU]
    handle_annual_vacation_keyboard = create_keyboard(actions=actions)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_state.get_last_bot_message_id(),
        text=handle_annual_vacation_text,
        inline_keyboard_markup=json.dumps(handle_annual_vacation_keyboard)
    )


def create_annual_vacation_cb(
        bot,
        user_state: UserStateManager,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Create annual vacation callback for {user_id}")
    user_state.state_machine.to_create_annual_vacation()
    user_state.save_state()

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_state.get_last_bot_message_id(),
        text=CREATE_ANNUAL_VACATION_TEXT
    )


def confirm_annual_vacation_cb(
        bot,
        user_state: UserStateManager,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Confirm annual vacation callback for {user_id}")
    # TODO: Добавить в будущем запрос для отправки отпуска на согласование
    # current_vacation = user_state.get_current_vacation()

    start_date, end_date = user_state.get_current_vacation_dates()
    confirm_annual_vacation_text = CONFIRM_ANNUAL_VACATION_TEXT_TEMPLATE.format(period=f"{start_date} - {end_date}")
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=confirm_annual_vacation_text,
        show_alert=False
    )
    back_to_main_menu_cb(bot, user_state, user_id, event, callback_data_value)


def back_to_main_menu_cb(
        bot,
        user_state: UserStateManager,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Handling back to main menu for user {user_id}")

    user_state.reset_current_vacation_and_limit()
    user_state.state_machine.to_main_menu()
    user_state.save_state()

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_state.get_last_bot_message_id(),
        text="Главное меню",  # TODO: Текст через actions
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
        # TODO: Сделать клавиатуру для главного меню через actions
    )


annual_vacation_callbacks = {
    Actions.HANDLE_ANNUAL_VACATION.value: handle_annual_vacation_cb,
    Actions.CREATE_ANNUAL_VACATION.value: create_annual_vacation_cb,
    Actions.CONFIRM_ANNUAL_VACATION.value: confirm_annual_vacation_cb,
    Actions.BACK_TO_MAIN_MENU: back_to_main_menu_cb
}


def annual_vacation_callback_dispatcher(bot, event: Event) -> None:
    user_id = event.from_chat
    user_state = UserStateManager.get_state(user_id)
    callback_data = event.data.get('callbackData')
    callback_data_prefix, callback_data_value = parse_callback_data(callback_data)
    callback = annual_vacation_callbacks.get(callback_data_prefix)

    if callback:
        logger.info(f"Found callback for callback_data: {callback_data}")
        callback(bot, user_state, user_id, event, callback_data_value)


def create_annual_vacation_from_dates_cb(
        bot,
        user_state: UserStateManager,
        user_id: str,
        event: Event,
) -> None:
    logger.info(f" Accept annual vacation callback for {user_id}")
    vacation_dates = event.data['text']
    start_date, end_date = parse_vacation_dates(vacation_dates)
    user_state.create_new_vacation(vacation_type=VacationType.ANNUAL_PAID,
                                   start_date=start_date,
                                   end_date=end_date)
    user_state.state_machine.to_confirm_annual_vacation()
    user_state.save_state()

    actions = [
        Actions.CONFIRM_ANNUAL_VACATION,
        Actions.BACK_TO_MAIN_MENU]
    handle_annual_vacation_keyboard = create_keyboard(actions=actions)

    handle_annual_vacation_dates_text = HANDLE_ANNUAL_VACATION_DATES_TEXT_TEMPLATE.format(
        period=f"{start_date} - {end_date}")

    bot.delete_messages(chat_id=user_id, msg_id=user_state.get_last_bot_message_id())
    response = bot.send_text(
        chat_id=user_id,
        text=handle_annual_vacation_dates_text,
        inline_keyboard_markup=json.dumps(handle_annual_vacation_keyboard)
    )
    logger.info(f"Response: {response.json()}")
    user_state.set_last_bot_message_id(response.json().get('msgId'))
    # TODO: Может делать авто сохранение состояния?
    user_state.save_state()


# TODO: Как будто это стоит вынести в отедльный модуль. Для сообщений диспетчиризация идет по состоянию.
#  Сделать одну фнукцию диспетчера для всех месседж колбежков?
def annual_vacation_message_cb(bot, event: Event) -> None:
    """Обрабатывает входящие сообщения, связанные с ежегодными отпусками."""
    user_id = event.from_chat
    user_state = UserStateManager.get_state(user_id)
    logger.info(f"annual_vacation_message_cb for user: {user_id}, state: {user_state.user_state}")

    # TODO: create_annual_vacation должно быть четко определено и возможно связано с actions
    if user_state.user_state != "create_annual_vacation":
        return

    logger.info(f"Event type: {event.type}")
    if event.type == EventType.NEW_MESSAGE:
        logger.info(f"Handling new message event for user {user_id}")
        create_annual_vacation_from_dates_cb(bot, user_state, user_id, event)
