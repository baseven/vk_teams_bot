import json
from src.states.state_machine import BotStateMachine

inline_keyboard_buttons = [
    [{"text": "Отпуска", "callbackData": "vacations", "style": "primary"}],
    [{"text": "Справки", "callbackData": "certificates", "style": "primary"}]

]


def start_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    bot.send_text(
        chat_id=event.from_chat,
        text="Главное меню",
        inline_keyboard_markup=json.dumps(inline_keyboard_buttons)
    )


def buttons_answer_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data['callbackData']
    # Переходы между состояниями в зависимости от нажатой кнопки
    if callback_data == "vacations":
        state_machine.to_vacations()
        state_machine.save_state()
        bot.send_text(chat_id=user_id,
                      text="Vacations Menu: Choose an option",
                      inline_keyboard_markup=[
                          [{"text": "Создать отпуск", "callbackData": "create_vacation"},
                           {"text": "Назад", "callbackData": "back"}]
                      ])
    elif callback_data == "create_vacation":
        bot.send_text(chat_id=user_id, text="Ваш отпуск создан")
    elif callback_data == "certificates":
        state_machine.to_certificates()
        state_machine.save_state()
        bot.send_text(chat_id=user_id,
                      text="Certificates Menu: Choose an option",
                      inline_keyboard_markup=[
                          [{"text": "Получить справку", "callbackData": "get_certificate"},
                           {"text": "Назад", "callbackData": "back"}]
                      ])
    elif callback_data == "get_certificate":
        bot.send_text(chat_id=user_id, text="Справка предоставлена")
    elif callback_data == "back":
        state_machine.to_main_menu()
        state_machine.save_state()
        bot.send_text(chat_id=user_id,
                      text="Главное меню",
                      inline_keyboard_markup=inline_keyboard_buttons)


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
