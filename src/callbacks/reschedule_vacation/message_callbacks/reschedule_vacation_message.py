import json
import logging

from bot.event import Event, EventType

from src.actions.reschedule_vacation import RescheduleVacationActions as Actions
from src.sessions import UserSession
from src.utils.validation_utils import validate_vacation_dates
from src.utils.keyboard_utils import create_keyboard

logger = logging.getLogger(__name__)

RESCHEDULE_VACATION_TEXT_TEMPLATE = "Вы уверены, что хотите перенести отпуск на выбранные даты {period}?"
CREATE_NEW_VACATION_TEXT = ("Пожалуйста, введите даты в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ, "
                            "на которые вы хотите перенести отпуск")

def reschedule_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
) -> None:
    """
    Handle the callback for rescheduling a vacation based on user-provided dates.

    Args:
        bot: The bot instance handling the message.
        user_session (UserSession): The current user session.
        user_id (str): The ID of the user.
        event (Event): The event containing user input, particularly the dates.

    Returns:
        None: Sends a message to the user depending on validation results and updates the session state.
    """
    is_valid, result = validate_vacation_dates(event.data['text'])
    if not is_valid:
        bot.delete_messages(
            chat_id=user_id,
            msg_id=user_session.get_last_bot_message_id()
        )
        error_message = result + '\n' + CREATE_NEW_VACATION_TEXT
        response = bot.send_text(
            chat_id=user_id,
            text=error_message,
        )
        user_session.set_last_bot_message_id(response.json().get('msgId'))
        user_session.save_session()
        return

    start_date, end_date = result
    user_session.set_new_vacation_dates(start_date, end_date)
    user_session.state_machine.to_confirm_vacation_reschedule()
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
    if state != Actions.ENTER_NEW_VACATION_DATES.callback_data:
        return

    logger.info(f"Event type: {event.type}")
    if event.type == EventType.NEW_MESSAGE:
        logger.info(f"Handling new message event for user {user_id}")
        reschedule_vacation_cb(bot, user_session, user_id, event)
