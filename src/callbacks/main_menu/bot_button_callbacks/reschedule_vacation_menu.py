import json
import logging

from bot.event import Event

from src.actions import RescheduleVacationActions as Actions
from src.data.vacation_limits import vacation_limits_dict
from src.data.vacation_schedule import vacation_schedule
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.utils import create_keyboard, create_vacation_keyboard

logger = logging.getLogger(__name__)

RESCHEDULE_VACATION_MENU_TEXT_TEMPLATE = (
    "Вывожу запланированные отпуска. Можете выбрать один из них для редактирования. "
    "Доступно дней для оформления отпуска: {available_days}, но можно оформить и другое количество."
)


def reschedule_vacation_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str = None
) -> None:
    logger.info(f"Reschedule vacation menu callback for {user_id}")
    user_session.state_machine.to_reschedule_vacation_menu()
    user_session.save_session()

    # TODO: Get vacation_limits from user_data
    available_days = vacation_limits_dict[VacationType.ANNUAL_PAID].available_days
    reschedule_vacation_menu_text = RESCHEDULE_VACATION_MENU_TEXT_TEMPLATE.format(available_days=available_days)

    # TODO: Add filter by vacation type
    vacation_keyboard = create_vacation_keyboard(
        planned_vacations=vacation_schedule,
        callback_prefix=Actions.SELECT_VACATION_TO_RESCHEDULE.value
    )

    actions = [
        Actions.BACK_TO_MAIN_MENU
    ]
    actions_keyboard = create_keyboard(actions=actions)
    reschedule_vacation_menu_keyboard = vacation_keyboard + actions_keyboard

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=reschedule_vacation_menu_text,
        inline_keyboard_markup=json.dumps(reschedule_vacation_menu_keyboard)
    )
