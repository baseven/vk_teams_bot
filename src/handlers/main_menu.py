import json
from src.keyboards.certificates import certificates_menu_buttons
from src.keyboards.vacations import vacations_menu_buttons
from src.states.state_machine import BotStateMachine


def handle_vacations(bot, state_machine, user_id):
    state_machine.to_vacations()
    state_machine.save_state()
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Vacations Menu: Choose an option",
        inline_keyboard_markup=vacations_menu_buttons
    )


def handle_certificates(bot, state_machine, user_id):
    state_machine.to_certificates()
    state_machine.save_state()
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Certificates Menu: Choose an option",
        inline_keyboard_markup=certificates_menu_buttons
    )


callback_handlers = {
    "vacations": handle_vacations,
    "certificates": handle_certificates
}


def buttons_answer_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data.get('callbackData')
    handler = callback_handlers.get(callback_data)
    if handler:
        handler(bot, state_machine, user_id)
