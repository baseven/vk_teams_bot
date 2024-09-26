from src.actions.bot_action import BotAction


class MainMenuActions:
    """Actions corresponding to the main menu buttons."""
    ANNUAL_VACATION_MENU = BotAction("annual_vacation_menu", "Оформить ежегодный отпуск")
    UNPAID_VACATION_MENU = BotAction("unpaid_vacation_menu", "Оформить отпуск без оплаты")
    LIMITS_AND_VACATIONS_MENU = BotAction("limits_and_vacations_menu", "Посмотреть лимиты и график отпусков")
    RESCHEDULE_VACATION_MENU = BotAction("reschedule_vacation_menu", "Перенести отпуск")
    CANCEL_VACATION_MENU = BotAction("cancel_vacation_menu", "Отменить отпуск")
