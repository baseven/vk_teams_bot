import json
from src.keyboards.vacations import vacations_menu_buttons
from src.keyboards.main_menu import main_menu_keyboard_buttons
from src.states.state_machine import BotStateMachine


def handle_vacation_action(bot, state_machine, user_id, event, message):
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=message,
        show_alert=False
    )
    state_machine.save_state()
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Vacations Menu: Choose an option",
        inline_keyboard_markup=vacations_menu_buttons
    )


def handle_annual_vacation(bot, state_machine, user_id, event):
    handle_vacation_action(bot, state_machine, user_id, event, "Ежегодный отпуск оформлен")


def handle_unpaid_vacation(bot, state_machine, user_id, event):
    handle_vacation_action(bot, state_machine, user_id, event, "Отпуск без оплаты оформлен")


def handle_view_limits_schedule(bot, state_machine, user_id, event):
    handle_vacation_action(bot, state_machine, user_id, event, "Лимиты и график отпусков просмотрены")


def handle_reschedule_vacation(bot, state_machine, user_id, event):
    handle_vacation_action(bot, state_machine, user_id, event, "Отпуск перенесен")


def handle_cancel_vacation(bot, state_machine, user_id, event):
    handle_vacation_action(bot, state_machine, user_id, event, "Отпуск отменен")


def handle_back(bot, state_machine, user_id, event):
    state_machine.to_main_menu()
    state_machine.save_state()
    bot.edit_text(
        chat_id=user_id,
        msg_id=state_machine.last_message_id,
        text="Главное меню",
        inline_keyboard_markup=main_menu_keyboard_buttons
    )


# TODO: There is a relationship with callbackData in vacations_menu_buttons. This needs to be refactored.
vacations_callback_handlers = {
    "annual_vacation": handle_annual_vacation,
    "unpaid_vacation": handle_unpaid_vacation,
    "view_limits_schedule": handle_view_limits_schedule,
    "reschedule_vacation": handle_reschedule_vacation,
    "cancel_vacation": handle_cancel_vacation,
    "back": handle_back
}


def vacations_callback_handler(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data.get('callbackData')
    handler = vacations_callback_handlers.get(callback_data)
    if handler:
        handler(bot, state_machine, user_id, event)
