from enum import Enum


class ActionBase:
    """Базовый класс для обработки callback_data и описания."""

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


class BaseActions(Enum):
    """Общие действия для всех меню."""
    BACK_TO_MAIN_MENU = ActionBase("back_to_main_menu", "Вернуться в главное меню")


class MainMenuActions(Enum):
    """Действия для главного меню."""
    ANNUAL_VACATION_MENU = ActionBase("annual_vacation_menu", "Оформить ежегодный отпуск")
    UNPAID_VACATION = ActionBase("unpaid_vacation", "Оформить отпуск без оплаты")
    VIEW_LIMITS_AND_SCHEDULE = ActionBase("view_limits_and_schedule", "Посмотреть лимиты и график отпусков")
    RESCHEDULE_VACATION = ActionBase("reschedule_vacation", "Перенести отпуск")
    CANCEL_VACATION = ActionBase("cancel_vacation", "Отменить отпуск")
    BACK_TO_MAIN_MENU = ActionBase("back_to_main_menu", "Вернуться в главное меню")


class AnnualVacationActions(Enum):
    """Действия для меню отпуска."""
    HANDLE_ANNUAL_VACATION = ActionBase("handle_annual_vacation", "")
    CREATE_ANNUAL_VACATION = ActionBase("create_annual_vacation", "Другие даты")
    CONFIRM_ANNUAL_VACATION = ActionBase("confirm_annual_vacation", "Оформить")
    BACK_TO_MAIN_MENU = ActionBase("back_to_main_menu", "Вернуться в главное меню")


class CancelVacationActions(Enum):
    """Действия для отмены отпуска."""
    SELECT_VACATION_TO_CANCEL = ActionBase("select_vacation_to_cancel", "")
    CONFIRM_VACATION_CANCELLATION = ActionBase("confirm_vacation_cancellation", "Удалить")
    BACK_TO_MAIN_MENU = ActionBase("back_to_main_menu", "Вернуться в главное меню")


class RescheduleVacationActions(Enum):
    """Действия для переноса отпуска."""
    SELECT_VACATION_TO_RESCHEDULE = ActionBase("select_vacation_to_reschedule", "")
    RESCHEDULE_VACATION = ActionBase("reschedule_vacation", "Перенести отпуск")
    CONFIRM_VACATION_RESCHEDULE = ActionBase("confirm_vacation_reschedule", "Оформить")
    BACK_TO_MAIN_MENU = ActionBase("back_to_main_menu", "Вернуться в главное меню")
