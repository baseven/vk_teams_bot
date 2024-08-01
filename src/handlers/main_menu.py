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
    if state_machine.last_message_id:
        bot.delete_messages(chat_id=event.from_chat, msg_id=state_machine.last_message_id)
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
    response = bot.send_text(chat_id=user_id,
                             text="Vacations Menu: Choose an option",
                             inline_keyboard_markup=vacations_buttons)
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()


def handle_create_vacation(bot, state_machine, user_id):
    response = bot.send_text(chat_id=user_id, text="Ваш отпуск создан")
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.to_vacations()  # Переход в состояние vacations
    state_machine.save_state()
    response = bot.send_text(chat_id=user_id,
                             text="Vacations Menu: Choose an option",
                             inline_keyboard_markup=vacations_buttons)
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()


def handle_certificates(bot, state_machine, user_id):
    state_machine.to_certificates()
    state_machine.save_state()
    response = bot.send_text(chat_id=user_id,
                             text="Certificates Menu: Choose an option",
                             inline_keyboard_markup=certificates_buttons)
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()


def handle_get_certificate(bot, state_machine, user_id):
    response = bot.send_text(chat_id=user_id, text="Справка предоставлена")
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.to_certificates()  # Переход в состояние certificates
    state_machine.save_state()
    response = bot.send_text(chat_id=user_id,
                             text="Certificates Menu: Choose an option",
                             inline_keyboard_markup=certificates_buttons)
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()


def handle_back(bot, state_machine, user_id):
    state_machine.to_main_menu()
    state_machine.save_state()
    response = bot.send_text(chat_id=user_id,
                             text="Главное меню",
                             inline_keyboard_markup=json.dumps(inline_keyboard_buttons))
    state_machine.last_message_id = response.json().get('msgId')
    state_machine.save_state()


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

    if state_machine.last_message_id:
        bot.delete_messages(chat_id=user_id, msg_id=state_machine.last_message_id)

    handler = callback_handlers.get(callback_data)
    if handler:
        handler(bot, state_machine, user_id)
    else:
        bot.send_text(chat_id=user_id, text="Неизвестная команда.")

# def restart_cb()


# def buttons_answer_cb_old(bot, event):
#     print(f'pre_state: {state_machine.state},'
#           f'callbackData: {event.data.get("callbackData")}')
#     if state_machine.state != 'main_menu':
#         print('Not in main menu')
#         return
#
#     if event.data['callbackData'] == "vacation":
#         state_machine.to_vacation()
#         bot.answer_callback_query(
#             query_id=event.data['queryId'],
#             text="Вы выбрали Отпуска",
#             show_alert=False
#         )
#
#     elif event.data['callbackData'] == "certificate":
#         bot.answer_callback_query(
#             query_id=event.data['queryId'],
#             text="Вы выбрали Справки",
#             show_alert=False
#         )
#     print(f'post_state: {state_machine.state}')
