import json
import logging
from bot.event import Event  # Импорт Event для типизации
from src.keyboards import main_menu_keyboard
from src.states.state_machine import BotStateMachine

logger = logging.getLogger(__name__)


def start_cb(bot, event: Event) -> None:
    """Обрабатывает команду /start от пользователя.

    Args:
        bot: Экземпляр бота.
        event (Event): Событие, содержащее данные команды.
    """
    user_id = event.from_chat
    logger.info(f"Received /start command from user {user_id}")

    state_machine = BotStateMachine.get_state(user_id)

    response = bot.send_text(
        chat_id=user_id,
        text="Главное меню",
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
    )

    logger.info(f"Response: {response.json()}")
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()
    logger.info(f"Sent main menu to user {user_id}")
