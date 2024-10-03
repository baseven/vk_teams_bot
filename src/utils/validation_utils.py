from datetime import datetime

from src.constants import DATE_FORMAT


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
