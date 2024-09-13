import json
import logging

from bot.event import Event  # Импорт Event для типизации

from src.actions import BaseActions as Actions
from src.sessions import UserSession
from src.utils import create_keyboard, format_limits_text, format_vacations_text

logger = logging.getLogger(__name__)


def view_limits_and_schedule_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"View limits and schedule callback for user {user_id}")
    user_session.state_machine.to_view_limits_and_schedule()
    user_session.save_session()

    vacations, limits = user_session.get_vacations_and_limits()

    limits_text = format_limits_text(limits)
    schedule_text = format_vacations_text(vacations)
    limits_and_schedule_text = f"{limits_text}\n\n{schedule_text}"
    actions = [
        Actions.BACK_TO_MAIN_MENU
    ]
    actions_keyboard = create_keyboard(actions=actions)
    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=limits_and_schedule_text,
        inline_keyboard_markup=json.dumps(actions_keyboard)
    )
