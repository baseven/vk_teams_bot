from src.actions.bot_action import BotAction
from src.states.main_menu import MainMenu

class MainMenuActions:
    """Действия, соответствующие кнопкам главного меню."""

    ANNUAL_VACATION_MENU = BotAction(
        callback_data=MainMenu.annual_vacation_menu.name,
        text="Оформить ежегодный отпуск"
    )
    UNPAID_VACATION_MENU = BotAction(
        callback_data=MainMenu.unpaid_vacation_menu.name,
        text="Оформить отпуск без оплаты"
    )
    LIMITS_AND_VACATIONS_MENU = BotAction(
        callback_data=MainMenu.limits_and_vacations_menu.name,
        text="Посмотреть лимиты и график отпусков"
    )
    RESCHEDULE_VACATION_MENU = BotAction(
        callback_data=MainMenu.reschedule_vacation_menu.name,
        text="Перенести отпуск"
    )
    CANCEL_VACATION_MENU = BotAction(
        callback_data=MainMenu.cancel_vacation_menu.name,
        text="Отменить отпуск"
    )
