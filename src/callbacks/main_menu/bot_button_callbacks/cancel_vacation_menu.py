import json
import logging

from bot.event import Event

from src.buttons.cancel_vacation import CancelVacationButtons as Buttons
from tests.data_fixtures.vacation_schedule import vacation_schedule
from src.sessions import UserSession
from src.utils.keyboard_utils import create_keyboard, create_vacation_keyboard

logger = logging.getLogger(__name__)


PLANNED_VACATION_TEXT = "Вывожу запланированные отпуска. Можете выбрать один из них для удаления."


def cancel_vacation_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"Cancel vacation menu callback for user {user_id}")

    user_session.state_machine.to_cancel_vacation_menu()
    user_session.save_session()

    # TODO: Add filter by vacation type
    vacation_keyboard = create_vacation_keyboard(
        vacations=vacation_schedule,
        callback_prefix=Buttons.SELECT_VACATION_TO_CANCEL.callback_data
    )

    buttons = [
        Buttons.BACK_TO_MAIN_MENU,
    ]
    actions_keyboard = create_keyboard(buttons=buttons)

    keyboard = vacation_keyboard + actions_keyboard
    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=PLANNED_VACATION_TEXT,
        inline_keyboard_markup=json.dumps(keyboard)
    )
