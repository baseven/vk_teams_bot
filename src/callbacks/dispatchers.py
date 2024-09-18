import logging

from bot.event import Event, EventType

from src.sessions import UserSession
from src.utils import parse_callback_data

logger = logging.getLogger(__name__)


def callback_dispatcher(bot, event: Event, callbacks: dict) -> None:
    """Dispatch bot button callbacks based on the user's state."""
    user_id = event.from_chat
    user_session = UserSession.get_session(user_id)
    callback_data = event.data.get('callbackData')
    callback_data_prefix, callback_data_value = parse_callback_data(callback_data)
    callback = callbacks.get(callback_data_prefix)

    if callback:
        logger.info(f"Found callback for callback_data: {callback_data}")
        callback(bot, user_session, user_id, event, callback_data_value)


def message_dispatcher(bot, event: Event, message_callbacks: dict) -> None:
    """Dispatch message callbacks based on the user's state."""
    user_id = event.from_chat
    user_session = UserSession.get_session(user_id)
    state = user_session.user_data.state
    callback = message_callbacks.get(state)

    if callback and event.type == EventType.NEW_MESSAGE:
        logger.info(f"Dispatching message handler for state: {state}")
        callback(bot, user_session, user_id, event)
