from datetime import datetime
from typing import List, Tuple

from src.constants import DATE_FORMAT
from src.messages.error_messages import ErrorMessages
from src.models import Vacation


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
            return False, ErrorMessages.DATE_FORMAT_ERROR

        start_date, end_date = vacation_dates.split('-')
        start_date_obj = datetime.strptime(start_date.strip(), DATE_FORMAT)
        end_date_obj = datetime.strptime(end_date.strip(), DATE_FORMAT)

        if start_date_obj > end_date_obj:
            return False, ErrorMessages.DATE_ORDER_ERROR

        if start_date_obj < datetime.now() or end_date_obj < datetime.now():
            return False, ErrorMessages.PAST_DATE_ERROR

        return True, (start_date_obj.strftime(DATE_FORMAT), end_date_obj.strftime(DATE_FORMAT))
    except ValueError:
        return False, ErrorMessages.DATE_FORMAT_ERROR

def check_vacation_overlap(
    new_start_date: datetime,
    new_end_date: datetime,
    existing_vacations: List[Vacation]
) -> Tuple[bool, str]:
    """
    Проверяет, пересекается ли новый отпуск с существующими отпусками.

    Args:
        new_start_date (datetime): Дата начала нового отпуска.
        new_end_date (datetime): Дата окончания нового отпуска.
        existing_vacations (List[Vacation]): Список существующих отпусков пользователя.

    Returns:
        Tuple[bool, str]:
            - (True, ""): Если пересечений нет.
            - (False, error_message): Если найдено пересечение, возвращает сообщение об ошибке.
    """
    for vacation in existing_vacations:
        if new_start_date <= vacation.end_date and new_end_date >= vacation.start_date:
            return False, ErrorMessages.OVERLAP_ERROR
    return True, ""