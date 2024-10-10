import json
import logging

from bot.event import Event

from src.buttons.annual_vacation import AnnualVacationButtons as Buttons
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard, create_vacation_keyboard

logger = logging.getLogger(__name__)


def handle_annual_vacation_menu(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data: str = None
) -> None:
    logger.info(f"Annual vacation menu callback for user {user_id}")

    user_session.state_machine.to_annual_vacation_menu()
    user_session.save_session()

    # TODO: limit or available_days?
    available_days = user_session.vacation_manager.get_limit_by_type(VacationType.ANNUAL_PAID)
    message_text = messages.main_menu.annual_vacation_menu.format(available_days=available_days)

    vacation_keyboard = create_vacation_keyboard(
        vacations=user_session.vacation_manager.get_vacations_by_type(VacationType.ANNUAL_PAID),
        callback_prefix=Buttons.HANDLE_ANNUAL_VACATION.callback_data
    )
    buttons = [
        Buttons.CREATE_ANNUAL_VACATION,
        Buttons.BACK_TO_MAIN_MENU
    ]
    actions_keyboard = create_keyboard(buttons=buttons)
    keyboard = vacation_keyboard + actions_keyboard

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.last_bot_message_id,
        text=message_text,
        inline_keyboard_markup=json.dumps(keyboard)
    )
