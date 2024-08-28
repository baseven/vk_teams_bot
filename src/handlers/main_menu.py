import json
from src.keyboards import main_menu_keyboard
from src.states.state_machine import BotStateMachine
from src.handlers.annual_vacation import handle_annual_vacation
from src.handlers.limits_and_schedule import handle_view_limits_and_schedule


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
        text="Меню отпусков: Выберите действие",
        inline_keyboard_markup=main_menu_keyboard
    )


def handle_unpaid_vacation(bot, state_machine, user_id, event):
    handle_vacation_action(bot, state_machine, user_id, event, "Отпуск без оплаты оформлен")


def handle_reschedule_vacation(bot, state_machine, user_id, event):
    handle_vacation_action(bot, state_machine, user_id, event, "Отпуск перенесен")


def handle_cancel_vacation(bot, state_machine, user_id, event):
    handle_vacation_action(bot, state_machine, user_id, event, "Отпуск отменен")


# TODO: There is a relationship with callbackData in vacations_menu_buttons. This needs to be refactored.
main_menu_cb_handlers = {
    "annual_vacation_menu": handle_annual_vacation,
    "unpaid_vacation": handle_unpaid_vacation,
    "view_limits_and_schedule": handle_view_limits_and_schedule,
    "reschedule_vacation": handle_reschedule_vacation,
    "cancel_vacation": handle_cancel_vacation,
}


def main_menu_cb(bot, event):
    user_id = event.from_chat
    state_machine = BotStateMachine.load_state(user_id)
    callback_data = event.data.get('callbackData')
    handler = main_menu_cb_handlers.get(callback_data)
    if handler:
        handler(bot, state_machine, user_id, event)
