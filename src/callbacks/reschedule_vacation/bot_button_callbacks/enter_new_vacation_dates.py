import json
import logging

from bot.event import Event

from src.buttons.reschedule_vacation import RescheduleVacationButtons as Buttons
from src.sessions import UserSession
from src.texts.messages import messages
from src.utils.keyboard_utils import create_keyboard

logger = logging.getLogger(__name__)


# TODO: Rename, because there should be a correspondence between the state and the name of the function.
# TODO: It is necessary to indicate what type of leave is being created, or we use the type of leave that was.
def enter_new_vacation_dates_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data: str
) -> None:
    logger.info(f"Create annual vacation callback for {user_id}")

    user_session.state_machine.to_enter_new_vacation_dates()
    user_session.save_session()

    buttons = [
        Buttons.BACK_TO_MAIN_MENU
    ]
    keyboard = create_keyboard(buttons=buttons)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.last_bot_message_id,
        text=messages.reschedule_vacation.enter_new_vacation_dates,
        inline_keyboard_markup=json.dumps(keyboard)
    )
