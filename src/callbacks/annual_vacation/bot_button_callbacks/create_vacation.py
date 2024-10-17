import json
import logging

from bot.event import Event

from src.buttons.annual_vacation import AnnualVacationButtons as Buttons
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard

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

    buttons = [
        Buttons.BACK_TO_MAIN_MENU
    ]
    keyboard = create_keyboard(buttons=buttons)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.last_bot_message_id,
        text=messages.annual_vacation.create_annual_vacation,
        inline_keyboard_markup=json.dumps(keyboard)
    )
