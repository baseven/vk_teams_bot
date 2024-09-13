import json
import logging

from bot.event import Event

from src.actions import BaseActions as Actions
from src.sessions import UserSession
from src.utils import create_keyboard

logger = logging.getLogger(__name__)

UNPAID_VACATION_MENU_TEXT = "UNPAID_VACATION_MENU"


def unpaid_vacation_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"Unpaid vacation menu callback for user {user_id}")
    user_session.state_machine.to_unpaid_vacation()
    user_session.save_session()

    actions = [
        Actions.BACK_TO_MAIN_MENU
    ]
    actions_keyboard = create_keyboard(actions=actions)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=UNPAID_VACATION_MENU_TEXT,
        inline_keyboard_markup=json.dumps(actions_keyboard)
    )
