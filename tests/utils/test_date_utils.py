from datetime import datetime, timedelta

from src.constants import DATE_FORMAT
from src.utils.validation_utils import validate_vacation_dates


def test_valid_vacation_dates():
    """
    Test valid vacation dates in DD.MM.YYYY format, dynamically using future dates.
    """
    start_date = (datetime.now() + timedelta(days=10)).strftime(DATE_FORMAT)
    end_date = (datetime.now() + timedelta(days=15)).strftime(DATE_FORMAT)

    vacation_dates = f"{start_date} - {end_date}"

    is_valid, dates = validate_vacation_dates(vacation_dates)
    assert is_valid
    assert dates == (start_date, end_date)


def test_invalid_vacation_date_format():
    """
    Test invalid date format.
    """
    is_valid, error_message = validate_vacation_dates("2024/01/01 - 2024/01/15")
    assert not is_valid
    assert error_message == "Неверный формат даты или символы. Пожалуйста, используйте формат DD.MM.YYYY - DD.MM.YYYY."


def test_single_date_error():
    """
    Test when only one date is provided.
    """
    is_valid, error_message = validate_vacation_dates("01.01.2024")
    assert not is_valid
    assert error_message == "Пожалуйста, укажите обе даты в формате DD.MM.YYYY - DD.MM.YYYY."


def test_start_date_later_than_end_date():
    """
    Test when start date is later than the end date.
    """
    is_valid, error_message = validate_vacation_dates("15.01.2024 - 01.01.2024")
    assert not is_valid
    assert error_message == "Дата начала не может быть позже даты окончания."


def test_vacation_dates_in_past():
    """
    Test when vacation dates are in the past.
    """
    is_valid, error_message = validate_vacation_dates("01.01.2020 - 15.01.2020")
    assert not is_valid
    assert error_message == "Дата не может быть в прошлом."
