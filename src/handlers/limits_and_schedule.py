import json
import logging
from typing import List
from bot.event import Event  # Импорт Event для типизации
from src.models.vacation import Vacation, Limit, VacationType
from src.data.vacation_limits import vacation_limits
from src.data.vacation_schedule import vacation_schedule
from src.keyboards import limits_and_schedule_keyboard

logger = logging.getLogger(__name__)


def handle_view_limits_and_schedule(bot, state_machine, user_id: str, event: Event) -> None:
    """Обрабатывает запрос на просмотр лимитов и графика отпусков.

    Args:
        bot: Экземпляр бота.
        state_machine: Машина состояний для пользователя.
        user_id (str): Идентификатор пользователя.
        event (Event): Данные события.
    """
    logger.info(f"Starting view limits and schedule process for user {user_id}")

    state_machine.to_view_limits_and_schedule()
    state_machine.save_state()

    # Загрузка лимитов и графика для пользователя
    user_limits: List[Limit] = vacation_limits
    user_schedule: List[Vacation] = vacation_schedule

    if not user_limits or not user_schedule:
        bot.send_text(chat_id=user_id, text="Информация о лимитах и графике отпусков отсутствует.")
        return

    # Формируем текстовое сообщение с лимитами и графиком
    limits_text = "Лимиты отпусков:\n" + "\n".join(
        [f"{limit.vacation_type.value}: {limit.available_days} дней" for limit in user_limits]
    )
    schedule_text = "График отпусков:\n" + "\n".join(
        [
            f"Тип: {vacation.vacation_type.value}, с {vacation.start_date.strftime('%d.%m.%Y')} по {vacation.end_date.strftime('%d.%m.%Y')}"
            for vacation in user_schedule]
    )

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=limits_text + "\n\n" + schedule_text,
        inline_keyboard_markup=json.dumps(limits_and_schedule_keyboard)
    )
