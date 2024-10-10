import json
import logging

from bot.event import Event

from src.buttons.main_menu import MainMenuButtons as Buttons
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard

logger = logging.getLogger(__name__)


def start_cb(bot, event: Event) -> None:
    user_id = event.from_chat

    logger.info(f"Received /start command from user {user_id}")

    user_session = UserSession(user_id)

    buttons = [
        Buttons.ANNUAL_VACATION_MENU,
        Buttons.UNPAID_VACATION_MENU,
        Buttons.LIMITS_AND_VACATIONS_MENU,
        Buttons.RESCHEDULE_VACATION_MENU,
        Buttons.CANCEL_VACATION_MENU,
    ]
    keyboard = create_keyboard(buttons=buttons)

    response = bot.send_text(
        chat_id=user_id,
        text=messages.commands.main_menu,
        inline_keyboard_markup=json.dumps(keyboard)
    )

    user_session.last_bot_message_id = response.json().get('msgId')
    user_session.save_session()
