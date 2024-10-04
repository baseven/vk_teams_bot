from bot.event import Event

from src.buttons.main_menu import MainMenuButtons as Buttons
from src.callbacks.dispatchers import callback_dispatcher
from src.callbacks.main_menu.bot_button_callbacks import (annual_vacation_menu_cb, cancel_vacation_menu_cb,
                                                          reschedule_vacation_menu_cb, limits_and_vacations_menu_cb,
                                                          unpaid_vacation_menu_cb)

main_menu_callbacks = {
    Buttons.ANNUAL_VACATION_MENU.callback_data: annual_vacation_menu_cb,
    Buttons.UNPAID_VACATION_MENU.callback_data: unpaid_vacation_menu_cb,
    Buttons.LIMITS_AND_VACATIONS_MENU.callback_data: limits_and_vacations_menu_cb,
    Buttons.RESCHEDULE_VACATION_MENU.callback_data: reschedule_vacation_menu_cb,
    Buttons.CANCEL_VACATION_MENU.callback_data: cancel_vacation_menu_cb,
}


def main_menu_callback_dispatcher(bot, event: Event) -> None:
    callback_dispatcher(bot=bot, event=event, callbacks=main_menu_callbacks)
