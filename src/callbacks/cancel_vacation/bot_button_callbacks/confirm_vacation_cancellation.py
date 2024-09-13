import json
import logging

from bot.event import Event

from src.callbacks.common_bot_button import back_to_main_menu_cb
from src.sessions import UserSession

logger = logging.getLogger(__name__)


CONFIRM_VACATION_CANCELLATION_TEXT_TEMPLATE = "Ежегодный отпуск {period} удален"


def confirm_vacation_cancellation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"Confirm cancel vacation callback for {user_id}")
    # TODO: Add a request to cancel a vacation in the future
    # current_vacation = user_session.get_current_vacation()

    start_date, end_date = user_session.get_current_vacation_dates()
    confirm_vacation_cancellation_text = CONFIRM_VACATION_CANCELLATION_TEXT_TEMPLATE.format(period=f"{start_date} - {end_date}")
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=confirm_vacation_cancellation_text,
        show_alert=False
    )
    back_to_main_menu_cb(bot, user_session, user_id, event, callback_data_value)
