import logging

from bot.event import Event

from src.callbacks.common_bot_button import back_to_main_menu_cb
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.text_utils import format_vacation_period

logger = logging.getLogger(__name__)


def confirm_vacation_reschedule_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Handling confirm change vacation for user {user_id}")

    start_date, end_date = user_session.get_new_vacation_dates()
    # TODO: How to determine the type of vacation?
    user_session.create_new_vacation(vacation_type=VacationType.ANNUAL_PAID,
                                     start_date=start_date,
                                     end_date=end_date)

    vacation_period = format_vacation_period(start_date=start_date, end_date=end_date)
    message_text = messages.reschedule_vacation.confirm_vacation_reschedule.format(period=vacation_period)
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=message_text,
        show_alert=False
    )

    back_to_main_menu_cb(bot, user_session, user_id, event, callback_data_value)

