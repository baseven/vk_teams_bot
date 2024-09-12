import json
import logging

from bot.event import Event

from src.actions import AnnualVacationActions as Actions
from src.data.vacation_limits import vacation_limits_dict
from src.data.vacation_schedule import vacation_schedule
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.utils import create_keyboard, create_vacation_keyboard

logger = logging.getLogger(__name__)

ANNUAL_VACATION_MENU_TEXT_TEMPLATE = (
    "Вывожу доступные плановые периоды. Можете выбрать один из них или выбрать другие даты. "
    "Доступно дней для оформления отпуска: {available_days}, но можно оформить и другое количество."
)


def annual_vacation_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"Annual vacation menu callback for user {user_id}")

    user_session.state_machine.to_annual_vacation_menu()
    user_session.save_session()

    annual_vacation_keyboard = create_vacation_keyboard(
        planned_vacations=vacation_schedule,
        callback_prefix=Actions.HANDLE_ANNUAL_VACATION.value
    )

    actions = [
        Actions.CREATE_ANNUAL_VACATION,
        Actions.BACK_TO_MAIN_MENU
    ]
    annual_vacation_keyboard2 = create_keyboard(actions=actions)

    annual_vacation_menu_keyboard = annual_vacation_keyboard + annual_vacation_keyboard2
    available_days = vacation_limits_dict[VacationType.ANNUAL_PAID].available_days
    annual_vacation_text = ANNUAL_VACATION_MENU_TEXT_TEMPLATE.format(available_days=available_days)

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=annual_vacation_text,
        inline_keyboard_markup=json.dumps(annual_vacation_menu_keyboard)
    )
