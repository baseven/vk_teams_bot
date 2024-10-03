from datetime import datetime

from src.constants import DATE_FORMAT
from src.models import Limit, Vacation


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
            f"Тип: {vacation.vacation_type}, с {vacation.start_date.strftime(DATE_FORMAT)} "
            f"по {vacation.end_date.strftime(DATE_FORMAT)}, статус: {vacation.status}"
            for vacation in vacations
        ]
    )
    return schedule_text

# TODO: Add tests
def format_vacation_period(start_date: datetime, end_date: datetime) -> str:
    """
    Formats the vacation period from datetime objects to a string in the format 'DD.MM.YYYY - DD.MM.YYYY'.

    Args:
        start_date (datetime): The start date of the vacation.
        end_date (datetime): The end date of the vacation.

    Returns:
        str: The formatted vacation period string.
    """
    return f"{start_date.strftime(DATE_FORMAT)} - {end_date.strftime(DATE_FORMAT)}"
