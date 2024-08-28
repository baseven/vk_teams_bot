import json
import logging

from src.data.vacation_limits import vacation_limits
from src.data.vacation_schedule import vacation_schedule

from src.keyboards import limits_and_schedule_keyboard

logger = logging.getLogger(__name__)


def handle_view_limits_and_schedule(bot, state_machine, user_id, event):
    logger.info(f"Starting view limits and schedule process for user {user_id}")
    state_machine.to_view_limits_and_schedule()
    state_machine.save_state()

    # Загрузка лимитов и графика для пользователя
    user_limits = vacation_limits
    user_schedule = vacation_schedule

    if not user_limits or not user_schedule:
        bot.send_text(chat_id=user_id, text="Информация о лимитах и графике отпусков отсутствует.")
        return

    # Формируем текстовое сообщение с лимитами и графиком
    limits_text = f"Лимиты отпусков:\nЕжегодный: {user_limits['annual']} дней\nБез оплаты: {user_limits['unpaid']} дней\n"
    schedule_text = "График отпусков:\n" + "\n".join(
        [f"Тип: {vacation['type']}, с {vacation['start']} по {vacation['end']}" for vacation in user_schedule]
    )

    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text=limits_text + "\n" + schedule_text,
        inline_keyboard_markup=json.dumps(limits_and_schedule_keyboard)
    )
