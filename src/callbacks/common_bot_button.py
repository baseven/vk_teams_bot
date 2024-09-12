import json
import logging

from bot.event import Event, EventType

from src.actions import AnnualVacationActions as Actions
from src.data.vacation_limits import vacation_limits_dict
from src.data.vacation_schedule import vacation_schedule
from src.keyboards import main_menu_keyboard
from src.models.vacation import VacationType
from src.sessions import UserSession
from src.utils import create_keyboard, create_vacation_keyboard, parse_callback_data, parse_vacation_dates

logger = logging.getLogger(__name__)

ANNUAL_VACATION_MENU_TEXT_TEMPLATE = (
    "Вывожу доступные плановые периоды. Можете выбрать один из них или выбрать другие даты. "
    "Доступно дней для оформления отпуска: {available_days}, но можно оформить и другое количество."
)
HANDLE_ANNUAL_VACATION_TEXT_TEMPLATE = "Оформить отпуск на {period} или вы хотите немного изменить даты?"
CONFIRM_ANNUAL_VACATION_TEXT_TEMPLATE = "Оформление ежегодного отпуска {period} отправлено на согласование"
CREATE_ANNUAL_VACATION_TEXT = "Введите период. Пожалуйста, укажите период в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ"
HANDLE_ANNUAL_VACATION_DATES_TEXT_TEMPLATE = "Вы точно хотите оформить отпуск на {period}?"


def back_to_main_menu_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Handling back to main menu for user {user_id}")

    user_session.reset_current_vacation_and_limit()
    user_session.state_machine.to_main_menu()
    user_session.save_session()

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text="Main menu",  # TODO: Add main menu text through actions
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
        # TODO: Generate main menu keyboard through actions
    )
