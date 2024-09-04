from typing import List
from src.models.vacation import Vacation


def create_vacation_buttons(
        planned_vacations: List[Vacation],
        callback_prefix: str,
        button_style: str
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

    for vacation in planned_vacations:
        start_date = vacation.start_date.strftime('%d.%m.%Y')
        end_date = vacation.end_date.strftime('%d.%m.%Y')
        callback_data = f"{callback_prefix}_{start_date}-{end_date}"

        button = {
            "text": f"{start_date} - {end_date}",
            "callbackData": callback_data,
            "style": button_style
        }

        buttons.append([button])

    return buttons
