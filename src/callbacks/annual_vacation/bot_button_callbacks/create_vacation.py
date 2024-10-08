import logging

from bot.event import Event

from src.sessions import UserSession
from src.texts.messages import messages

logger = logging.getLogger(__name__)


def create_annual_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data: str
) -> None:
    logger.info(f"Create annual vacation callback for {user_id}")
    user_session.state_machine.to_create_annual_vacation()
    user_session.save_session()

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=messages.annual_vacation.create_annual_vacation
    )
