from datetime import datetime, timedelta

import pytest

from src.utils import (
    create_keyboard,
    create_vacation_keyboard,
    parse_callback_data,
    validate_vacation_dates,
    format_limits_text,
    format_vacations_text,
    CALLBACK_DATA_SEPARATOR
)
from src.styles import ButtonStyle

def test_create_keyboard(sample_actions):
    """
    Test the create_keyboard function.
    """
    keyboard = create_keyboard(sample_actions)

    assert len(keyboard) == len(sample_actions)
    for idx, action in enumerate(sample_actions):
        button = keyboard[idx][0]
        assert button['text'] == action.text
        assert button['callbackData'] == action.callback_data
        assert button['style'] == ButtonStyle.PRIMARY.value

def test_create_keyboard_empty_actions():
    """
    Test create_keyboard with empty actions list.
    """
    with pytest.raises(ValueError):
        create_keyboard([])

def test_create_vacation_keyboard(sample_vacations):
    """
    Test the create_vacation_keyboard function.
    """
    callback_prefix = "vacation"
    keyboard = create_vacation_keyboard(sample_vacations, callback_prefix)

    assert len(keyboard) == len(sample_vacations)
    for idx, vacation in enumerate(sample_vacations, 1):
        button = keyboard[idx - 1][0]
        expected_callback_data = f"{callback_prefix}{CALLBACK_DATA_SEPARATOR}{vacation.vacation_id}"
        expected_text = (
            f"{idx}. С {vacation.start_date.strftime('%d.%m.%Y')} по {vacation.end_date.strftime('%d.%m.%Y')}, "
            f"тип: {vacation.vacation_type}, статус: {vacation.status}"
        )
        assert button['text'] == expected_text
        assert button['callbackData'] == expected_callback_data
        assert button['style'] == ButtonStyle.PRIMARY.value

def test_parse_callback_data():
    """
    Test the parse_callback_data function.
    """
    callback_data = "prefix|value"
    prefix, value = parse_callback_data(callback_data)
    assert prefix == "prefix"
    assert value == "value"

    callback_data = "noprefix"
    prefix, value = parse_callback_data(callback_data)
    assert prefix == "noprefix"
    assert value == ""


def test_valid_vacation_dates():
    """
    Test valid vacation dates in DD.MM.YYYY format, dynamically using future dates.
    """
    # Дата начала через 10 дней от текущей даты
    start_date = (datetime.now() + timedelta(days=10)).strftime("%d.%m.%Y")
    # Дата окончания через 15 дней от текущей даты
    end_date = (datetime.now() + timedelta(days=15)).strftime("%d.%m.%Y")

    # Формируем строку для тестирования
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
            f"Тип: {vacation.vacation_type}, с {vacation.start_date.strftime('%d.%m.%Y')} "
            f"по {vacation.end_date.strftime('%d.%m.%Y')}, статус: {vacation.status}"
        )
        assert expected_line in text

def test_format_vacations_text_no_vacations():
    """
    Test format_vacations_text with empty vacations list.
    """
    text = format_vacations_text([])
    assert text == "График отпусков не найден."