from datetime import datetime
from typing import List, Dict, Any, Tuple, Union

from src.actions.bot_action import BotAction
from src.models.vacation import Vacation, Limit
from src.styles import ButtonStyle


DATE_FORMAT = "%d.%m.%Y"

CALLBACK_DATA_SEPARATOR = '|'


def create_keyboard(
    actions: List[BotAction],
    button_style: ButtonStyle = ButtonStyle.PRIMARY
) -> List[List[Dict[str, Any]]]:
    """
    Create a keyboard layout based on a list of actions and a button style.

    Args:
        actions (List[BotAction]): A list of actions to create buttons for.
        button_style (ButtonStyle, optional): The style to apply to each button. Defaults to ButtonStyle.PRIMARY.

    Returns:
        List[List[Dict[str, Any]]]: A generated keyboard layout.

    Raises:
        ValueError: If the actions list is empty.
    """
    if not actions:
        raise ValueError("The 'actions' list cannot be empty.")

    return [
        [{
            "text": action.text,
            "callbackData": action.callback_data,
            "style": button_style.value
        }]
        for action in actions
    ]


def create_vacation_keyboard(
    vacations: List[Vacation],
    callback_prefix: str,
    button_style: ButtonStyle = ButtonStyle.PRIMARY
) -> List[List[Dict[str, str]]]:
    """
    Create buttons for vacations with the specified callback prefix and button style.

    Args:
        vacations (List[Vacation]): List of vacations.
        callback_prefix (str): Prefix for callback data.
        button_style (ButtonStyle, optional): Style of the button for the interface. Defaults to ButtonStyle.PRIMARY.

    Returns:
        List[List[Dict[str, str]]]: List of buttons for the bot interface.
    """
    buttons = []

    for idx, vacation in enumerate(vacations, 1):
        callback_data = f"{callback_prefix}{CALLBACK_DATA_SEPARATOR}{vacation.vacation_id}"
        button_text = (
            f"{idx}. С {vacation.start_date.strftime('%d.%m.%Y')} по {vacation.end_date.strftime('%d.%m.%Y')}, "
            f"тип: {vacation.vacation_type}, статус: {vacation.status}"
        )

        button = {
            "text": button_text,
            "callbackData": callback_data,
            "style": button_style.value
        }

        buttons.append([button])

    return buttons


def parse_callback_data(callback_data: str) -> Tuple[str, str]:
    """
    Split callback_data into prefix and value.

    Args:
        callback_data (str): The callbackData string to split.

    Returns:
        Tuple[str, str]: A tuple containing the prefix and value.
    """
    if CALLBACK_DATA_SEPARATOR in callback_data:
        prefix, value = callback_data.split(CALLBACK_DATA_SEPARATOR, 1)
        return prefix, value
    return callback_data, ""


def validate_vacation_dates(vacation_dates: str):
    """
    Validate vacation dates provided in the format "DD.MM.YYYY - DD.MM.YYYY".

    Args:
        vacation_dates (str): A string containing the start and end dates in the format "DD.MM.YYYY - DD.MM.YYYY".

    Returns:
        Tuple[bool, Union[str, Tuple[datetime, datetime]]]:
            - (True, (start_date, end_date)): If validation is successful, returns a tuple with start and end datetime objects.
            - (False, error_message): If validation fails, returns False and an error message explaining the issue.
    """
    try:
        if "-" not in vacation_dates:
            return False, "Пожалуйста, укажите обе даты в формате DD.MM.YYYY - DD.MM.YYYY."

        start_date, end_date = vacation_dates.split('-')
        start_date_obj = datetime.strptime(start_date.strip(), DATE_FORMAT)
        end_date_obj = datetime.strptime(end_date.strip(), DATE_FORMAT)

        if start_date_obj > end_date_obj:
            return False, "Дата начала не может быть позже даты окончания."

        if start_date_obj < datetime.now() or end_date_obj < datetime.now():
            return False, "Дата не может быть в прошлом."

        return True, (start_date_obj.strftime(DATE_FORMAT), end_date_obj.strftime(DATE_FORMAT))
    except ValueError:
        return False, "Неверный формат даты или символы. Пожалуйста, используйте формат DD.MM.YYYY - DD.MM.YYYY."


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
        [f"{limit.vacation_type}: {limit.available_days} дней" for limit in limits]
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
            f"Тип: {vacation.vacation_type}, с {vacation.start_date.strftime('%d.%m.%Y')} по {vacation.end_date.strftime('%d.%m.%Y')}, статус: {vacation.status}"
            for vacation in vacations
        ]
    )
    return schedule_text
