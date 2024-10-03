import json
import logging

from bot.event import Event

from src.actions.annual_vacation import AnnualVacationActions as Actions
from src.sessions import UserSession
from src.utils.keyboard_utils import create_keyboard
from src.utils.text_utils import format_vacation_period

logger = logging.getLogger(__name__)

HANDLE_ANNUAL_VACATION_TEXT_TEMPLATE = "Оформить отпуск на {period} или вы хотите немного изменить даты?"


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
    handle_annual_vacation_text = HANDLE_ANNUAL_VACATION_TEXT_TEMPLATE.format(period=vacation_period)

    actions = [
        Actions.CONFIRM_ANNUAL_VACATION,
        Actions.CREATE_ANNUAL_VACATION,
        Actions.BACK_TO_MAIN_MENU]
    handle_annual_vacation_keyboard = create_keyboard(actions=actions)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=handle_annual_vacation_text,
        inline_keyboard_markup=json.dumps(handle_annual_vacation_keyboard)
    )
