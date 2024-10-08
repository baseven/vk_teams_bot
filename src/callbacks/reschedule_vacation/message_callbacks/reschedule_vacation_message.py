import json
import logging

from bot.event import Event, EventType

from src.buttons.reschedule_vacation import RescheduleVacationButtons as Buttons
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.validation_utils import validate_vacation_dates, check_vacation_overlap
from src.utils.keyboard_utils import create_keyboard
from src.utils.text_utils import format_vacation_period

logger = logging.getLogger(__name__)


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
        error_message = result + '\n' + messages.reschedule_vacation.create_new_vacation
        response = bot.send_text(
            chat_id=user_id,
            text=error_message,
        )
        user_session.set_last_bot_message_id(response.json().get('msgId'))
        user_session.save_session()
        return

    start_date, end_date = result
    existing_vacations, _ = user_session.get_vacations_and_limits()
    is_valid, result = check_vacation_overlap(new_start_date=start_date,
                                                     new_end_date=end_date,
                                                     existing_vacations=existing_vacations)
    if not is_valid:
        bot.delete_messages(
            chat_id=user_id,
            msg_id=user_session.get_last_bot_message_id()
        )
        error_message = result + '\n' + messages.reschedule_vacation.create_new_vacation
        response = bot.send_text(
            chat_id=user_id,
            text=error_message,
        )
        user_session.set_last_bot_message_id(response.json().get('msgId'))
        user_session.save_session()
        return

    user_session.set_new_vacation_dates(start_date, end_date)
    user_session.state_machine.to_confirm_vacation_reschedule()
    user_session.save_session()

    vacation_period = format_vacation_period(start_date=start_date, end_date=end_date)
    message_text = messages.reschedule_vacation.reschedule_vacation.format(period=vacation_period)

    buttons = [
        Buttons.CONFIRM_VACATION_RESCHEDULE,
        Buttons.BACK_TO_MAIN_MENU]
    keyboard = create_keyboard(buttons=buttons)

    bot.delete_messages(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id()
    )

    response = bot.send_text(
        chat_id=user_id,
        text=message_text,
        inline_keyboard_markup=json.dumps(keyboard)
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

    # TODO: The  state should be clearly defined and possibly linked to buttons
    if state != Buttons.ENTER_NEW_VACATION_DATES.callback_data:
        return

    logger.info(f"Event type: {event.type}")
    if event.type == EventType.NEW_MESSAGE:
        logger.info(f"Handling new message event for user {user_id}")
        reschedule_vacation_cb(bot, user_session, user_id, event)
