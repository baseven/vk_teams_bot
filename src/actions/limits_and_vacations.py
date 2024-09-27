from src.actions.bot_action import BotAction

class LimitsAndVacationsActions:
    BACK_TO_MAIN_MENU = BotAction(
        callback_data="back_to_main_menu",
        text="Вернуться в главное меню"
    )
