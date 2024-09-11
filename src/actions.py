from enum import Enum


class BaseActions(Enum):
    """Общие действия для всех меню с их описанием на русском."""
    BACK_TO_MAIN_MENU = ("back_to_main_menu", "Вернуться в главное меню")

    def __init__(self, callback_data, description):
        self.callback_data = callback_data
        self.description = description

    @property
    def value(self):
        """Возвращает значение callbackData для использования в ботах."""
        return self.callback_data

    @property
    def text(self):
        """Возвращает текстовое описание кнопки."""
        return self.description


class MainMenuActions(BaseActions):
    """Действия для главного меню."""

    ANNUAL_VACATION_MENU = ("annual_vacation_menu", "Оформить ежегодный отпуск")
    UNPAID_VACATION = ("unpaid_vacation", "Оформить отпуск без оплаты")
    VIEW_LIMITS_AND_SCHEDULE = ("view_limits_and_schedule", "Посмотреть лимиты и график отпусков")
    RESCHEDULE_VACATION = ("reschedule_vacation", "Перенести отпуск")
    CANCEL_VACATION = ("cancel_vacation", "Отменить отпуск")


class AnnualVacationActions(BaseActions):
    """Действия для меню отпуска."""
    HANDLE_ANNUAL_VACATION = ("handle_annual_vacation", "")
    CREATE_ANNUAL_VACATION = ("create_annual_vacation", "Другие даты")
    CONFIRM_ANNUAL_VACATION = ("confirm_annual_vacation", "Оформить")


class EditVacationMenuActions(BaseActions):
    """Действия для изменения отпуска."""
    RESCHEDULE_VACATION = ("reschedule_vacation", "Перенести отпуск")
    CANCEL_VACATION = ("cancel_vacation", "Отменить отпуск")
