from bot.event import Event

from src.actions import MainMenuActions as Actions
from src.callbacks.dispatchers import callback_dispatcher
from src.callbacks.main_menu.bot_button_callbacks import (annual_vacation_menu_cb, cancel_vacation_menu_cb,
                                                          reschedule_vacation_menu_cb, view_limits_and_schedule_cb,
                                                          unpaid_vacation_menu_cb)

main_menu_callbacks = {
    Actions.ANNUAL_VACATION_MENU.value: annual_vacation_menu_cb,
    Actions.UNPAID_VACATION.value: unpaid_vacation_menu_cb,
    Actions.VIEW_LIMITS_AND_SCHEDULE.value: view_limits_and_schedule_cb,
    Actions.RESCHEDULE_VACATION.value: reschedule_vacation_menu_cb,
    Actions.CANCEL_VACATION.value: cancel_vacation_menu_cb,
}


def main_menu_callback_dispatcher(bot, event: Event) -> None:
    callback_dispatcher(bot=bot, event=event, callbacks=main_menu_callbacks)
