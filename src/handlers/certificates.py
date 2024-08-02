import json
from src.keyboards.main_menu import main_menu_keyboard_buttons
from src.keyboards.certificates import certificates_menu_buttons
from src.states.state_machine import BotStateMachine


def handle_get_certificate(bot, state_machine, user_id, event):
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text="Справка предоставлена",
        show_alert=False
    )
    state_machine.to_certificates()
    state_machine.save_state()
    response = bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Certificates Menu: Choose an option",
        inline_keyboard_markup=certificates_menu_buttons
    )


def handle_back(bot, state_machine, user_id, event):
    state_machine.to_main_menu()
    state_machine.save_state()
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Главное меню",
        inline_keyboard_markup=main_menu_keyboard_buttons
    )


certificates_callback_handlers = {
    "get_certificate": handle_get_certificate,
    "back": handle_back
}


def certificates_callback_handler(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data.get('callbackData')
    handler = certificates_callback_handlers.get(callback_data)
    if handler:
        handler(bot, state_machine, user_id, event)
