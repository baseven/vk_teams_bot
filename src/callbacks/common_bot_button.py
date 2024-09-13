import json
import logging

from bot.event import Event

from src.actions import MainMenuActions as Actions
from src.sessions import UserSession
from src.utils import create_keyboard

logger = logging.getLogger(__name__)
# TODO: Add main menu text through actions
MAIN_MENU_TEXT = "Главное меню"


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

    actions = [
        Actions.ANNUAL_VACATION_MENU,
        Actions.UNPAID_VACATION,
        Actions.VIEW_LIMITS_AND_SCHEDULE,
        Actions.RESCHEDULE_VACATION,
        Actions.CANCEL_VACATION,
    ]
    main_menu_keyboard = create_keyboard(actions=actions)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=MAIN_MENU_TEXT,
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
    )
