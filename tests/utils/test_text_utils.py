from datetime import datetime

from src.constants import DATE_FORMAT
from src.utils.text_utils import format_limits_text, format_vacations_text, format_vacation_period


def test_format_limits_text(sample_limits):
    """
    Test the format_limits_text function.
    """
    text = format_limits_text(sample_limits)
    for limit in sample_limits:
        expected_line = f"{limit.vacation_type}: {limit.available_days} дней"
        assert expected_line in text


def test_format_limits_text_no_limits():
    """
    Test format_limits_text with empty limits.
    """
    text = format_limits_text([])
    assert text == "Лимиты отпусков не найдены."


def test_format_vacations_text(sample_vacations):
    """
    Test the format_vacations_text function.
    """
    text = format_vacations_text(sample_vacations)
    for vacation in sample_vacations:
        expected_line = (
            f"Тип: {vacation.vacation_type}, с {vacation.start_date.strftime(DATE_FORMAT)} "
            f"по {vacation.end_date.strftime(DATE_FORMAT)}, статус: {vacation.status}"
        )
        assert expected_line in text


def test_format_vacations_text_no_vacations():
    """
    Test format_vacations_text with empty vacations list.
    """
    text = format_vacations_text([])
    assert text == "График отпусков не найден."


def test_format_vacation_period():
    """
    Test the formatting of vacation dates to a string.
    """
    start_date = datetime(2024, 10, 1)
    end_date = datetime(2024, 10, 15)
    expected = "01.10.2024 - 15.10.2024"

    result = format_vacation_period(start_date, end_date)
    assert result == expected