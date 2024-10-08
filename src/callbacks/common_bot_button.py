import json
import logging

from bot.event import Event

from src.buttons.main_menu import MainMenuButtons as Buttons
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard

logger = logging.getLogger(__name__)


def back_to_main_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Back to main menu callback for user {user_id}")

    user_session.reset_current_vacation_and_limit()
    user_session.state_machine.to_main_menu()
    user_session.save_session()

    buttons = [
        Buttons.ANNUAL_VACATION_MENU,
        Buttons.UNPAID_VACATION_MENU,
        Buttons.LIMITS_AND_VACATIONS_MENU,
        Buttons.RESCHEDULE_VACATION_MENU,
        Buttons.CANCEL_VACATION_MENU,
    ]
    keyboard = create_keyboard(buttons=buttons)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=messages.commands.main_menu,
        inline_keyboard_markup=json.dumps(keyboard)
    )
