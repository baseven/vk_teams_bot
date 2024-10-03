import logging

from bot.event import Event

from src.callbacks.common_bot_button import back_to_main_menu_cb
from src.sessions import UserSession
from src.utils.text_utils import format_vacation_period

logger = logging.getLogger(__name__)

CONFIRM_ANNUAL_VACATION_TEXT_TEMPLATE = "Оформление ежегодного отпуска {period} отправлено на согласование"


def confirm_annual_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Confirm annual vacation callback for {user_id}")
    user_session.state_machine.to_confirm_annual_vacation()
    user_session.save_session()
    # TODO: Add vacation approval request in the future
    # current_vacation = user_session.get_current_vacation()

    start_date, end_date = user_session.get_current_vacation_dates()
    vacation_period = format_vacation_period(start_date=start_date, end_date=end_date)
    confirm_annual_vacation_text = CONFIRM_ANNUAL_VACATION_TEXT_TEMPLATE.format(period=vacation_period)
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=confirm_annual_vacation_text,
        show_alert=False
    )
    back_to_main_menu_cb(bot, user_session, user_id, event, callback_data_value)
