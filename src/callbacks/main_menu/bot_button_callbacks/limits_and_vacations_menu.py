import json
import logging

from bot.event import Event

from src.buttons.limits_and_vacations import LimitsAndVacationsButtons as Buttons
from src.sessions import UserSession
from src.utils.text_utils import format_limits_text, format_vacations_text
from src.utils.keyboard_utils import create_keyboard
from texts.messages import messages

logger = logging.getLogger(__name__)


def limits_and_vacations_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data: str = None
) -> None:
    logger.info(f"View limits and vacations callback for user {user_id}")

    user_session.state_machine.to_limits_and_vacations_menu()
    user_session.save_session()

    # TODO: Should texts be generated from templates that will be stored in src/texts/messages/messages.json?
    limits_text = format_limits_text(user_session.vacation_manager.limits)
    vacations_text = format_vacations_text(user_session.vacation_manager.vacations)
    message_text = f"{limits_text}\n\n{vacations_text}"

    buttons = [
        Buttons.BACK_TO_MAIN_MENU
    ]
    keyboard = create_keyboard(buttons=buttons)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.last_bot_message_id,
        text=message_text,
        inline_keyboard_markup=json.dumps(keyboard)
    )
