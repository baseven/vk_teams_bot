import json
import logging

from bot.event import Event

from src.buttons.limits_and_vacations import LimitsAndVacationsButtons as Buttons
from src.sessions import UserSession
from src.utils.text_utils import format_limits_text, format_vacations_text
from src.utils.keyboard_utils import create_keyboard

logger = logging.getLogger(__name__)


#TODO: Should texts be generated from templates that will be stored in src/texts/messages/messages.json?
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

    vacations, limits = user_session.get_vacations_and_limits()
    limits_text = format_limits_text(limits)
    schedule_text = format_vacations_text(vacations)
    limits_and_schedule_text = f"{limits_text}\n\n{schedule_text}"

    buttons = [
        Buttons.BACK_TO_MAIN_MENU
    ]
    keyboard = create_keyboard(buttons=buttons)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=limits_and_schedule_text,
        inline_keyboard_markup=json.dumps(keyboard)
    )
