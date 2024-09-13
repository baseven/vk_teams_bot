import json
import logging

from bot.event import Event

from src.actions import CancelVacationActions as Actions
from src.utils import create_keyboard
from src.sessions import UserSession

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

    user_session.state_machine.to_cancel_vacation()
    user_session.set_current_vacation(vacation_id=callback_data_value)
    user_session.save_session()

    start_date, end_date = user_session.get_current_vacation_dates()
    select_vacation_to_cancel_text = SELECT_VACATION_TO_CANCEL_TEXT_TEMPLATE.format(period=f"{start_date} - {end_date}")

    actions = [
        Actions.CONFIRM_VACATION_CANCELLATION,
        Actions.BACK_TO_MAIN_MENU
    ]
    select_vacation_to_cancel_keyboard = create_keyboard(actions=actions)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=select_vacation_to_cancel_text,
        inline_keyboard_markup=json.dumps(select_vacation_to_cancel_keyboard)
    )
