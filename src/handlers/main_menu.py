import json
from src.states.state_machine import BotStateMachine

inline_keyboard_buttons = [
    [{"text": "Отпуска", "callbackData": "vacations", "style": "primary"}],
    [{"text": "Справки", "callbackData": "certificates", "style": "primary"}]
]

vacations_buttons = json.dumps([
    [{"text": "Создать отпуск", "callbackData": "create_vacation"},
     {"text": "Назад", "callbackData": "back"}]
])

certificates_buttons = json.dumps([
    [{"text": "Получить справку", "callbackData": "get_certificate"},
     {"text": "Назад", "callbackData": "back"}]
])


def start_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    response = bot.send_text(
        chat_id=event.from_chat,
        text="Главное меню",
        inline_keyboard_markup=json.dumps(inline_keyboard_buttons)
    )
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()


def handle_vacations(bot, state_machine, user_id):
    state_machine.to_vacations()
    state_machine.save_state()
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Vacations Menu: Choose an option",
        inline_keyboard_markup=vacations_buttons
    )


def handle_create_vacation(bot, state_machine, user_id, event):
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text="Ваш отпуск создан",
        show_alert=False
    )
    state_machine.to_vacations()
    state_machine.save_state()
    response = bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Vacations Menu: Choose an option",
        inline_keyboard_markup=vacations_buttons
    )


def handle_certificates(bot, state_machine, user_id):
    state_machine.to_certificates()
    state_machine.save_state()
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Certificates Menu: Choose an option",
        inline_keyboard_markup=certificates_buttons
    )


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
        inline_keyboard_markup=certificates_buttons
    )


def handle_back(bot, state_machine, user_id):
    state_machine.to_main_menu()
    state_machine.save_state()
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Главное меню",
        inline_keyboard_markup=json.dumps(inline_keyboard_buttons)
    )


callback_handlers = {
    "vacations": handle_vacations,
    "create_vacation": handle_create_vacation,
    "certificates": handle_certificates,
    "get_certificate": handle_get_certificate,
    "back": handle_back
}


def buttons_answer_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data['callbackData']

    handler = callback_handlers.get(callback_data)
    if handler:
        if callback_data in ["create_vacation", "get_certificate"]:
            handler(bot, state_machine, user_id, event)
        else:
            handler(bot, state_machine, user_id)
    else:
        bot.edit_text(
            chat_id=user_id,
            msg_id=state_machine.last_message_id,
            text="Неизвестная команда."
        )
