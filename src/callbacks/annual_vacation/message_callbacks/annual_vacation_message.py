import json
import logging

from bot.event import Event, EventType

from src.actions.annual_vacation import AnnualVacationActions as Actions
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.utils import create_keyboard, parse_vacation_dates

logger = logging.getLogger(__name__)


HANDLE_ANNUAL_VACATION_DATES_TEXT_TEMPLATE = "Вы точно хотите оформить отпуск на {period}?"


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


# TODO: Consider moving this to a separate module. For message_callbacks handling, the dispatcher should work by state.
#  Implement a unified dispatcher for all message_callbacks callbacks.
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
