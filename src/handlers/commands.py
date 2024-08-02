import logging
from src.keyboards.main_menu import main_menu_keyboard_buttons
from src.states.state_machine import BotStateMachine

logger = logging.getLogger(__name__)


def start_cb(bot, event):
    user_id = event.from_chat
    logger.info(f"Received /start command from user {user_id}")

    state_machine = BotStateMachine.load_state(user_id)
    response = bot.send_text(
        chat_id=event.from_chat,
        text="Главное меню",
        inline_keyboard_markup=main_menu_keyboard_buttons
    )
    logger.info(f"Response: {response.json()}")
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()
    logger.info(f"Sent main menu to user {user_id}")

