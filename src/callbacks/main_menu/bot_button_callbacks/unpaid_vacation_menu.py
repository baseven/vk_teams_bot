import json
import logging

from bot.event import Event

from src.buttons.unpaid_vacation import UnpaidVacationButtons as Buttons
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard

logger = logging.getLogger(__name__)


def unpaid_vacation_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data: str = None
) -> None:
    logger.info(f"Unpaid vacation menu callback for user {user_id}")

    user_session.state_machine.to_unpaid_vacation_menu()
    user_session.save_session()

    buttons = [
        Buttons.BACK_TO_MAIN_MENU
    ]
    keyboard = create_keyboard(buttons=buttons)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=messages.main_menu.unpaid_vacation_menu,
        inline_keyboard_markup=json.dumps(keyboard)
    )
