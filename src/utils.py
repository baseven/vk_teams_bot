from typing import List, Tuple

from src.actions import AnnualVacationActions
from src.models.vacation import Vacation
from src.styles import ButtonStyle

CALLBACK_DATA_SEPARATOR = '|'


def create_keyboard(
        actions: List[AnnualVacationActions],
        button_style: ButtonStyle = ButtonStyle.PRIMARY
) -> List[List[dict]]:
    """
    Создает клавиатуру на основе списка действий (actions) и стиля кнопки.

    Args:
        actions (List[VacationMenuActions]): Список действий, для которых нужно создать кнопки.
        button_style (ButtonStyle, optional): Стиль кнопки. По умолчанию PRIMARY.

    Returns:
        List[List[dict]]: Сгенерированная клавиатура.
    """
    return [
        [{"text": action.text, "callbackData": action.value, "style": button_style.value}]
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
