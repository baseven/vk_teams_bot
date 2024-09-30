import json
import logging

from bot.event import Event

from src.actions.reschedule_vacation import RescheduleVacationActions as Actions
from src.sessions import UserSession
from src.utils import create_keyboard

logger = logging.getLogger(__name__)

BOT_TEXT_TEMPLATE = "Вы действительно хотите перенести выбранный отпуск {period}?"


def confirm_vacation_selection_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"confirm_vacation_selection_cb {user_id}")
    user_session.state_machine.to_confirm_vacation_selection()
    user_session.set_current_vacation(vacation_id=callback_data_value)
    user_session.save_session()

    start_date, end_date = user_session.get_current_vacation_dates()
    bot_text = BOT_TEXT_TEMPLATE.format(period=f"{start_date} - {end_date}")
    actions = [
        Actions.ENTER_NEW_VACATION_DATES,
        Actions.BACK_TO_MAIN_MENU
    ]
    bot_inline_keyboard = create_keyboard(actions=actions)
    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=bot_text,
        inline_keyboard_markup=json.dumps(bot_inline_keyboard)
    )
