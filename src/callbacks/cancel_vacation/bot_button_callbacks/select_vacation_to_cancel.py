import json
import logging

from bot.event import Event

from src.buttons.cancel_vacation import CancelVacationButtons as Buttons
from src.utils.keyboard_utils import create_keyboard
from src.sessions import UserSession
from src.utils.text_utils import format_vacation_period

logger = logging.getLogger(__name__)

SELECT_VACATION_TO_CANCEL_TEXT_TEMPLATE = "Удалить отпуск {period}?"


def select_vacation_to_cancel_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"Handling cancel planned vacation for user {user_id}")

    user_session.state_machine.to_select_vacation_to_cancel()
    user_session.set_current_vacation(vacation_id=callback_data_value)
    user_session.save_session()

    start_date, end_date = user_session.get_current_vacation_dates()
    vacation_period = format_vacation_period(start_date=start_date, end_date=end_date)
    select_vacation_to_cancel_text = SELECT_VACATION_TO_CANCEL_TEXT_TEMPLATE.format(period=vacation_period)

    buttons = [
        Buttons.CONFIRM_VACATION_CANCELLATION,
        Buttons.BACK_TO_MAIN_MENU
    ]
    keyboard = create_keyboard(buttons=buttons)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=select_vacation_to_cancel_text,
        inline_keyboard_markup=json.dumps(keyboard)
    )
