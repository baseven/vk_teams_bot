import json
import logging

from bot.event import Event

from src.buttons.cancel_vacation import CancelVacationButtons as Buttons
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard, create_vacation_keyboard

logger = logging.getLogger(__name__)


def handle_cancel_vacation_menu(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data: str = None
) -> None:
    logger.info(f"Cancel vacation menu callback for user {user_id}")

    user_session.state_machine.to_cancel_vacation_menu()
    user_session.save_session()

    vacation_keyboard = create_vacation_keyboard(
        vacations=user_session.vacation_manager.vacations,
        callback_prefix=Buttons.SELECT_VACATION_TO_CANCEL.callback_data
    )
    buttons = [
        Buttons.BACK_TO_MAIN_MENU,
    ]
    actions_keyboard = create_keyboard(buttons=buttons)
    keyboard = vacation_keyboard + actions_keyboard

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.last_bot_message_id,
        text=messages.main_menu.cancel_vacation_menu,
        inline_keyboard_markup=json.dumps(keyboard)
    )
