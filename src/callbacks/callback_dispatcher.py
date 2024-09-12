import logging

from bot.event import Event

from src.sessions import UserSession
from src.utils import parse_callback_data

logger = logging.getLogger(__name__)


def callback_dispatcher(bot, event: Event, callbacks: dict) -> None:
    user_id = event.from_chat
    user_session = UserSession.get_session(user_id)
    callback_data = event.data.get('callbackData')
    callback_data_prefix, callback_data_value = parse_callback_data(callback_data)
    callback = callbacks.get(callback_data_prefix)

    if callback:
        logger.info(f"Found callback for callback_data: {callback_data}")
        callback(bot, user_session, user_id, event, callback_data_value)
