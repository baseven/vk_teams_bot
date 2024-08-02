import json

vacations_menu_buttons = json.dumps([
    [{"text": "Оформить ежегодный отпуск", "callbackData": "annual_vacation", "style": "primary"}],
    [{"text": "Оформить отпуск без оплаты", "callbackData": "unpaid_vacation", "style": "primary"}],
    [{"text": "Посмотреть лимиты и график отпусков", "callbackData": "view_limits_schedule", "style": "primary"}],
    [{"text": "Перенести отпуск", "callbackData": "reschedule_vacation", "style": "primary"}],
    [{"text": "Отменить отпуск", "callbackData": "cancel_vacation", "style": "primary"}],
    [{"text": "Назад", "callbackData": "back"}]
])
