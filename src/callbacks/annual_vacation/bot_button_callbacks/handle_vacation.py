import json
import logging

from bot.event import Event

from src.buttons.annual_vacation import AnnualVacationButtons as Buttons
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard
from src.utils.text_utils import format_vacation_period

logger = logging.getLogger(__name__)


def handle_annual_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Handle annual vacation callback for {user_id}")

    user_session.state_machine.to_handle_annual_vacation()
    user_session.set_current_vacation(vacation_id=callback_data_value)
    user_session.save_session()

    start_date, end_date = user_session.get_current_vacation_dates()
    vacation_period = format_vacation_period(start_date=start_date, end_date=end_date)
    message_text = messages.anual_vacation.handle_annual_vacation.format(period=vacation_period)

    buttons = [
        Buttons.CONFIRM_ANNUAL_VACATION,
        Buttons.CREATE_ANNUAL_VACATION,
        Buttons.BACK_TO_MAIN_MENU
    ]
    keyboard = create_keyboard(buttons=buttons)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=message_text,
        inline_keyboard_markup=json.dumps(keyboard)
    )
