import json
import logging

from bot.event import Event

from src.buttons.reschedule_vacation import RescheduleVacationButtons as Buttons
from tests.data_fixtures.vacation_limits import vacation_limits_dict
from tests.data_fixtures.vacation_schedule import vacation_schedule
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard, create_vacation_keyboard

logger = logging.getLogger(__name__)


def reschedule_vacation_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str, event: Event,
        callback_data: str = None
) -> None:
    logger.info(f"Reschedule vacation menu callback for {user_id}")

    user_session.state_machine.to_reschedule_vacation_menu()
    user_session.save_session()

    # TODO: Get vacation_limits from user_data
    available_days = vacation_limits_dict[VacationType.ANNUAL_PAID].available_days
    message_text = messages.main_menu.reschedule_vacation_menu.format(available_days=available_days)

    # TODO: Add filter by vacation type
    vacation_keyboard = create_vacation_keyboard(
        vacations=vacation_schedule,
        callback_prefix=Buttons.CONFIRM_VACATION_SELECTION.callback_data
    )

    buttons = [
        Buttons.BACK_TO_MAIN_MENU
    ]
    actions_keyboard = create_keyboard(buttons=buttons)
    keyboard = vacation_keyboard + actions_keyboard

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=message_text,
        inline_keyboard_markup=json.dumps(keyboard)
    )
