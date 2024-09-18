from typing import List

from src.actions import BaseActions
from src.models.vacation import Vacation, Limit
from src.styles import ButtonStyle

CALLBACK_DATA_SEPARATOR = '|'


from enum import Enum

def create_keyboard(
        actions: List[Enum],  # Общий тип для перечислений
        button_style: ButtonStyle = ButtonStyle.PRIMARY
) -> List[List[dict]]:
    """
    Создает клавиатуру на основе списка действий (actions) и стиля кнопки.

    Args:
        actions (List[Enum]): Список действий, для которых нужно создать кнопки.
        button_style (ButtonStyle, optional): Стиль кнопки. По умолчанию PRIMARY.

    Returns:
        List[List[dict]]: Сгенерированная клавиатура.
    """
    return [
        [{"text": action.value.text, "callbackData": action.value.value, "style": button_style.value}]
        for action in actions
    ]



def create_vacation_keyboard(
        planned_vacations: List['Vacation'],  # Assuming Vacation is a custom class
        callback_prefix: str,
        button_style: ButtonStyle = ButtonStyle.PRIMARY
) -> list[list[dict[str, str]]]:
    """Создает кнопки для плановых отпусков с указанным префиксом callback и стилем кнопки.

    Args:
        planned_vacations (List[Vacation]): Список запланированных отпусков.
        callback_prefix (str): Префикс для callback данных.
        button_style (str): Стиль кнопки для интерфейса.

    Returns:
        list[list[dict[str, str]]]: Список кнопок для интерфейса бота.
    """
    buttons = []

    for idx, vacation in enumerate(planned_vacations, 1):
        vacation_id = vacation.vacation_id
        vacation_type = vacation.vacation_type
        start_date = vacation.start_date.strftime('%d.%m.%Y')
        end_date = vacation.end_date.strftime('%d.%m.%Y')
        status = vacation.status  # Получаем статус отпуска

        callback_data = f"{callback_prefix}{CALLBACK_DATA_SEPARATOR}{vacation_id}"
        button_text = f"{idx}. {vacation_type}, с {start_date} по {end_date}, статус: {status}"

        button = {
            "text": button_text,
            "callbackData": callback_data,
            "style": button_style.value
        }

        buttons.append([button])

    return buttons


def parse_callback_data(callback_data: str) -> list[str] | tuple[str, str]:
    """
    Разделяет callback_data на префикс и значение.

    Args:
        callback_data (str): Строка callbackData, которую нужно разделить.

    Returns:
        tuple[str, str]: Префикс и значение, если разделитель найден, или (callback_data, "") если разделителя нет.
    """
    if CALLBACK_DATA_SEPARATOR in callback_data:
        return callback_data.split(CALLBACK_DATA_SEPARATOR, 1)
    return callback_data, ""


# TODO: Refactor and check if needed
def parse_vacation_dates(vacation_dates: str) -> tuple[str, str]:
    start_date, end_date = vacation_dates.split('-')
    return start_date.strip(), end_date.strip()


def format_limits_text(limits: list[Limit]) -> str:
    """
    Formats the user's vacation limits into a readable string.

    Args:
        limits (list[Limit]): List of limits associated with the user.

    Returns:
        str: Formatted string showing the vacation limits.
    """
    if not limits:
        return "Лимиты отпусков не найдены."

    limits_text = "Лимиты отпусков:\n" + "\n".join(
        [f"{limit.vacation_type.value}: {limit.available_days} дней" for limit in limits]
    )
    return limits_text


def format_vacations_text(vacations: list[Vacation]) -> str:
    """
    Formats the user's vacation schedule into a readable string.

    Args:
        vacations (list[Vacation]): List of vacations associated with the user.

    Returns:
        str: Formatted string showing the vacation schedule.
    """
    if not vacations:
        return "График отпусков не найден."

    schedule_text = "График отпусков:\n" + "\n".join(
        [
            f"Тип: {vacation.vacation_type.value}, с {vacation.start_date.strftime('%d.%m.%Y')} по {vacation.end_date.strftime('%d.%m.%Y')}, статус: {vacation.status.value}"
            for vacation in vacations
        ]
    )
    return schedule_text
