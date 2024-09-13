import json
import logging

from bot.event import Event, EventType

from src.actions import RescheduleVacationActions as Actions
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.utils import create_keyboard, parse_vacation_dates

logger = logging.getLogger(__name__)

RESCHEDULE_VACATION_TEXT_TEMPLATE = "Вы точно хотите оформить отпуск на {period}?"


def reschedule_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
) -> None:
    logger.info(f"Reschedule vacation callback for user {user_id}")
    vacation_dates = event.data['text']
    start_date, end_date = parse_vacation_dates(vacation_dates)
    user_session.set_new_vacation_dates(start_date, end_date)
    user_session.state_machine.to_confirm_reschedule_vacation()
    user_session.save_session()

    actions = [
        Actions.CONFIRM_VACATION_RESCHEDULE,
        Actions.BACK_TO_MAIN_MENU]
    reschedule_vacation_keyboard = create_keyboard(actions=actions)
    reschedule_vacation_text = RESCHEDULE_VACATION_TEXT_TEMPLATE.format(
        period=f"{start_date} - {end_date}")

    bot.delete_messages(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id()
    )
    response = bot.send_text(
        chat_id=user_id,
        text=reschedule_vacation_text,
        inline_keyboard_markup=json.dumps(reschedule_vacation_keyboard)
    )
    logger.info(f"Response: {response.json()}")
    user_session.set_last_bot_message_id(response.json().get('msgId'))
    user_session.save_session()


def reschedule_vacation_message_cb(bot, event: Event) -> None:
    """Handles incoming messages related to rescheduling vacations."""
    user_id = event.from_chat
    user_session = UserSession.get_session(user_id)
    state = user_session.user_data.state
    logger.info(f"reschedule_vacation_message_cb for user: {user_id}, state: {state}")

    # TODO: The  state should be clearly defined and possibly linked to actions
    if state != "entering_new_vacation_dates":
        return

    logger.info(f"Event type: {event.type}")
    if event.type == EventType.NEW_MESSAGE:
        logger.info(f"Handling new message event for user {user_id}")
        reschedule_vacation_cb(bot, user_session, user_id, event)
