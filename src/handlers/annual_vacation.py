import json
import logging

from bot.event import Event, EventType

from src.actions import AnnualVacationActions as Actions
from src.data.vacation_limits import vacation_limits_dict
from src.data.vacation_schedule import vacation_schedule
from src.keyboards import main_menu_keyboard
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.utils import create_keyboard, create_vacation_keyboard, parse_callback_data, parse_vacation_dates

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
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"Annual vacation menu callback for user {user_id}")

    user_session.state_machine.to_annual_vacation_menu()
    user_session.save_session()

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
        msg_id=user_session.get_last_bot_message_id(),
        text=annual_vacation_text,
        inline_keyboard_markup=json.dumps(annual_vacation_menu_keyboard)
    )


def handle_annual_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Handle annual vacation callback for {user_id}")

    user_session.state_machine.to_handle_annual_vacation()
    user_session.set_current_vacation(vacation_id=callback_data_value)
    user_session.save_session()

    start_date, end_date = user_session.get_current_vacation_dates()
    handle_annual_vacation_text = HANDLE_ANNUAL_VACATION_TEXT_TEMPLATE.format(period=f"{start_date}- {end_date}")

    actions = [
        Actions.CONFIRM_ANNUAL_VACATION,
        Actions.CREATE_ANNUAL_VACATION,
        Actions.BACK_TO_MAIN_MENU]
    handle_annual_vacation_keyboard = create_keyboard(actions=actions)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=handle_annual_vacation_text,
        inline_keyboard_markup=json.dumps(handle_annual_vacation_keyboard)
    )


def create_annual_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Create annual vacation callback for {user_id}")
    user_session.state_machine.to_create_annual_vacation()
    user_session.save_session()

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=CREATE_ANNUAL_VACATION_TEXT
    )


def confirm_annual_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Confirm annual vacation callback for {user_id}")
    # TODO: Add vacation approval request in the future
    # current_vacation = user_session.get_current_vacation()

    start_date, end_date = user_session.get_current_vacation_dates()
    confirm_annual_vacation_text = CONFIRM_ANNUAL_VACATION_TEXT_TEMPLATE.format(period=f"{start_date} - {end_date}")
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=confirm_annual_vacation_text,
        show_alert=False
    )
    back_to_main_menu_cb(bot, user_session, user_id, event, callback_data_value)


def back_to_main_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Handling back to main menu for user {user_id}")

    user_session.reset_current_vacation_and_limit()
    user_session.state_machine.to_main_menu()
    user_session.save_session()

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text="Main menu",  # TODO: Add main menu text through actions
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
        # TODO: Generate main menu keyboard through actions
    )


annual_vacation_callbacks = {
    Actions.HANDLE_ANNUAL_VACATION.value: handle_annual_vacation_cb,
    Actions.CREATE_ANNUAL_VACATION.value: create_annual_vacation_cb,
    Actions.CONFIRM_ANNUAL_VACATION.value: confirm_annual_vacation_cb,
    Actions.BACK_TO_MAIN_MENU: back_to_main_menu_cb
}


def annual_vacation_callback_dispatcher(bot, event: Event) -> None:
    user_id = event.from_chat
    user_session = UserSession.get_session(user_id)
    callback_data = event.data.get('callbackData')
    callback_data_prefix, callback_data_value = parse_callback_data(callback_data)
    callback = annual_vacation_callbacks.get(callback_data_prefix)

    if callback:
        logger.info(f"Found callback for callback_data: {callback_data}")
        callback(bot, user_session, user_id, event, callback_data_value)


def create_annual_vacation_from_dates_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
) -> None:
    logger.info(f"Accept annual vacation callback for {user_id}")
    vacation_dates = event.data['text']
    start_date, end_date = parse_vacation_dates(vacation_dates)
    user_session.create_new_vacation(vacation_type=VacationType.ANNUAL_PAID,
                                     start_date=start_date,
                                     end_date=end_date)
    user_session.state_machine.to_confirm_annual_vacation()
    user_session.save_session()

    actions = [
        Actions.CONFIRM_ANNUAL_VACATION,
        Actions.BACK_TO_MAIN_MENU]
    handle_annual_vacation_keyboard = create_keyboard(actions=actions)

    handle_annual_vacation_dates_text = HANDLE_ANNUAL_VACATION_DATES_TEXT_TEMPLATE.format(
        period=f"{start_date} - {end_date}")

    bot.delete_messages(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id()
    )
    response = bot.send_text(
        chat_id=user_id,
        text=handle_annual_vacation_dates_text,
        inline_keyboard_markup=json.dumps(handle_annual_vacation_keyboard)
    )
    logger.info(f"Response: {response.json()}")
    user_session.set_last_bot_message_id(response.json().get('msgId'))
    user_session.save_session()


# TODO: Consider moving this to a separate module. For message handling, the dispatcher should work by state.
#  Implement a unified dispatcher for all message callbacks.
def annual_vacation_message_cb(bot, event: Event) -> None:
    """Handles incoming messages related to annual vacations."""
    user_id = event.from_chat
    user_session = UserSession.get_session(user_id)
    state = user_session.user_data.state
    logger.info(f"annual_vacation_message_cb for user: {user_id}, state: {state}")

    # TODO: The create_annual_vacation state should be clearly defined and possibly linked to actions
    if state != "create_annual_vacation":
        return

    logger.info(f"Event type: {event.type}")
    if event.type == EventType.NEW_MESSAGE:
        logger.info(f"Handling new message event for user {user_id}")
        create_annual_vacation_from_dates_cb(bot, user_session, user_id, event)
