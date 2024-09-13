import json
import logging

from bot.event import Event, EventType

from src.actions import RescheduleVacationActions as Actions
from src.data.vacation_limits import vacation_limits_dict
from src.callbacks.common_bot_button import back_to_main_menu_cb
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.utils import create_keyboard, create_vacation_keyboard

logger = logging.getLogger(__name__)

CONFIRM_RESCHEDULE_VACATION_TEXT_TEMPLATE = "Перенесенный отпуск {period} отправлено на согласование"


def confirm_reschedule_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Handling confirm change vacation for user {user_id}")

    vacation_dates = event.data['text']
    start_date, end_date = user_session.get_new_vacation_dates()
    # TODO: How to determine the type of vacation?
    user_session.create_new_vacation(vacation_type=VacationType.ANNUAL_PAID,
                                     start_date=start_date,
                                     end_date=end_date)

    confirm_reschedule_vacation_text = CONFIRM_RESCHEDULE_VACATION_TEXT_TEMPLATE.format(period=f"{start_date} - {end_date}")
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=confirm_reschedule_vacation_text,
        show_alert=False
    )

    back_to_main_menu_cb(bot, user_session, user_id, event, callback_data_value)

