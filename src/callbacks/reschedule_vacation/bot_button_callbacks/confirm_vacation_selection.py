import json
import logging

from bot.event import Event

from src.buttons.reschedule_vacation import RescheduleVacationButtons as Buttons
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard
from src.utils.text_utils import format_vacation_period

logger = logging.getLogger(__name__)


def confirm_vacation_selection_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data: str = None
) -> None:
    logger.info(f"confirm_vacation_selection_cb {user_id}")

    user_session.vacation_manager.set_current_vacation_and_limit(vacation_id=callback_data)
    user_session.state_machine.to_confirm_vacation_selection()
    user_session.save_session()

    start_date, end_date = user_session.vacation_manager.get_current_vacation_dates()
    vacation_period = format_vacation_period(start_date=start_date, end_date=end_date)
    message_text = messages.reschedule_vacation.confirm_vacation_selection.format(period=vacation_period)

    buttons = [
        Buttons.ENTER_NEW_VACATION_DATES,
        Buttons.BACK_TO_MAIN_MENU
    ]
    keyboard = create_keyboard(buttons=buttons)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.last_bot_message_id,
        text=message_text,
        inline_keyboard_markup=json.dumps(keyboard)
    )
