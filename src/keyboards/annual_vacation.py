import json

#TODO: Предусмотреть возможность динамического формирования кнопок с датами.
# И то что запланированных дней може не быть
annual_vacation_buttons = [
    [{"text": "Другие даты", "callbackData": "create_new_vacation", "style": "primary"}],
    [{"text": "Вернуться в главное меню", "callbackData": "back_to_main_menu", "style": "primary"}]
]

confirm_period_keyboard = [
    [{"text": "Оформить", "callbackData": "confirm_planned_vacation", "style": "primary"}],
    [{"text": "Изменить", "callbackData": "create_new_vacation", "style": "primary"}],
    [{"text": "Вернуться в главное меню", "callbackData": "back_to_main_menu", "style": "primary"}]
]

accept_period_keyboard = [
    [{"text": "Оформить", "callbackData": "confirm_planned_vacation", "style": "primary"}],
    [{"text": "Вернуться в главное меню", "callbackData": "back_to_main_menu", "style": "primary"}]
]