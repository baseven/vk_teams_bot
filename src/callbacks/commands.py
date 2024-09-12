import json
import logging
from bot.event import Event
from src.keyboards import main_menu_keyboard
from src.sessions import UserSession

logger = logging.getLogger(__name__)


def start_cb(bot, event: Event) -> None:
    """Обрабатывает команду /start от пользователя.

    Args:
        bot: Экземпляр бота.
        event (Event): Событие, содержащее данные команды.
    """
    user_id = event.from_chat
    logger.info(f"Received /start command from user {user_id}")
    user_session = UserSession.get_session(user_id)

    response = bot.send_text(
        chat_id=user_id,
        text="Главное меню",
        inline_keyboard_markup=json.dumps(main_menu_keyboard)
    )

    logger.info(f"Response: {response.json()}")
    last_bot_message_id = response.json().get('msgId')
    user_session.set_last_bot_message_id(last_bot_message_id)
    user_session.save_session()
    logger.info(f"Sent main menu to user {user_id}")
