from bot.event import Event

from src.actions import MainMenuActions as Actions
from src.callbacks.callback_dispatcher import callback_dispatcher
from src.callbacks.main_menu.bot_button_callbacks import (annual_vacation_menu_cb, cancel_vacation_menu_cb,
                                                          reschedule_vacation_menu_cb, view_limits_and_schedule_cb,
                                                          unpaid_vacation_menu_cb)

main_menu_callbacks = {
    Actions.ANNUAL_VACATION_MENU: annual_vacation_menu_cb,
    Actions.UNPAID_VACATION: unpaid_vacation_menu_cb,
    Actions.VIEW_LIMITS_AND_SCHEDULE: view_limits_and_schedule_cb,
    Actions.RESCHEDULE_VACATION: reschedule_vacation_menu_cb,
    Actions.CANCEL_VACATION: cancel_vacation_menu_cb,
}


def main_menu_callback_dispatcher(bot, event: Event) -> None:
    callback_dispatcher(bot=bot, event=event, callbacks=main_menu_callbacks)
