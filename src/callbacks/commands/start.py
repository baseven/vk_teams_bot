import json
import logging

from bot.event import Event

from src.actions.main_menu import MainMenuActions as Actions
from src.sessions import UserSession
from src.utils.keyboard_utils import create_keyboard

logger = logging.getLogger(__name__)
# TODO: Add main menu text through actions
MAIN_MENU_TEXT = "Главное меню"


def start_cb(bot, event: Event) -> None:
    user_id = event.from_chat
    logger.info(f"Received /start command from user {user_id}")
    user_session = UserSession.get_session(user_id)

    actions = [
        Actions.ANNUAL_VACATION_MENU,
        Actions.UNPAID_VACATION_MENU,
        Actions.LIMITS_AND_VACATIONS_MENU,
        Actions.RESCHEDULE_VACATION_MENU,
        Actions.CANCEL_VACATION_MENU,
    ]
    main_menu_keyboard = create_keyboard(actions=actions)
    logger.info(f"Main menu keyboard: {main_menu_keyboard}")

    response = bot.send_text(
        chat_id=user_id,
        text=MAIN_MENU_TEXT,
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
    )

    last_bot_message_id = response.json().get('msgId')
    user_session.set_last_bot_message_id(last_bot_message_id)
    user_session.save_session()
