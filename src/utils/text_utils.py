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
            f"Тип: {vacation.vacation_type}, с {vacation.start_date.strftime('%d.%m.%Y')} по {vacation.end_date.strftime('%d.%m.%Y')}, статус: {vacation.status}"
            for vacation in vacations
        ]
    )
    return schedule_text
