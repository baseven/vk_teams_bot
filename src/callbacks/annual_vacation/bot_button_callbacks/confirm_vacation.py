import logging

from bot.event import Event

from src.callbacks.common_bot_button import back_to_main_menu_cb
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.text_utils import format_vacation_period

logger = logging.getLogger(__name__)


def confirm_annual_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data: str
) -> None:
    logger.info(f"Confirm annual vacation callback for {user_id}")

    user_session.state_machine.to_confirm_annual_vacation()
    user_session.save_session()

    current_vacation_dates = user_session.vacation_manager.get_current_vacation_dates()
    new_vacation_dates = user_session.vacation_manager.get_new_vacation_dates()

    if current_vacation_dates and not new_vacation_dates:
        vacation_period = format_vacation_period(start_date=current_vacation_dates[0],
                                                 end_date=current_vacation_dates[1])
        message_text = messages.annual_vacation.confirm_annual_vacation.format(period=vacation_period)

    elif new_vacation_dates and not current_vacation_dates:
        vacation_period = format_vacation_period(start_date=new_vacation_dates[0],
                                                 end_date=new_vacation_dates[1])
        message_text = messages.annual_vacation.confirm_annual_vacation.format(period=vacation_period)

    else:
        old_vacation_period = format_vacation_period(start_date=current_vacation_dates[0],
                                                     end_date=current_vacation_dates[1])
        new_vacation_period = format_vacation_period(start_date=new_vacation_dates[0],
                                                     end_date=new_vacation_dates[1])
        message_text = messages.annual_vacation.confirm_annual_vacation_reschedule.format(
            old_period=old_vacation_period,
            new_period=new_vacation_period)

    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=message_text,
        show_alert=False
    )

    back_to_main_menu_cb(bot, user_session, user_id, event, callback_data)
