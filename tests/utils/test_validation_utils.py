from datetime import datetime, timedelta


from src.messages.error_messages import ErrorMessages
from src.utils.validation_utils import validate_vacation_dates, check_vacation_overlap
from src.utils.text_utils import format_vacation_period


def test_valid_vacation_dates():
    """
    Test valid vacation dates in DD.MM.YYYY format, dynamically using future dates.
    """
    start_date = (datetime.today() + timedelta(days=10))
    end_date = (datetime.today() + timedelta(days=15))

    vacation_dates = format_vacation_period(start_date, end_date)

    is_valid, dates = validate_vacation_dates(vacation_dates)
    assert is_valid
    assert dates[0].date() == start_date.date()
    assert dates[1].date() == end_date.date()


def test_invalid_vacation_date_format():
    """
    Test invalid date format.
    """
    is_valid, error_message = validate_vacation_dates("2024/01/01 - 2024/01/15")
    assert not is_valid
    assert error_message == ErrorMessages.DATE_FORMAT_ERROR


def test_single_date_error():
    """
    Test when only one date is provided.
    """
    is_valid, error_message = validate_vacation_dates("01.01.2024")
    assert not is_valid
    assert error_message == ErrorMessages.DATE_FORMAT_ERROR


def test_start_date_later_than_end_date():
    """
    Test when start date is later than the end date.
    """
    is_valid, error_message = validate_vacation_dates("15.01.2024 - 01.01.2024")
    assert not is_valid
    assert error_message == ErrorMessages.DATE_ORDER_ERROR


def test_vacation_dates_in_past():
    """
    Test when vacation dates are in the past.
    """
    is_valid, error_message = validate_vacation_dates("01.01.2020 - 15.01.2020")
    assert not is_valid
    assert error_message == ErrorMessages.PAST_DATE_ERROR

def test_check_vacation_overlap_no_overlap(sample_vacations):
    """
    Тестирование случая, когда новый отпуск не пересекается с существующими отпусками.
    """
    new_start_date = datetime.now() + timedelta(days=30)
    new_end_date = new_start_date + timedelta(days=5)

    is_valid, error_message = check_vacation_overlap(
        new_start_date, new_end_date, sample_vacations
    )

    assert is_valid
    assert error_message == ""

def test_check_vacation_overlap_with_overlap(sample_vacations):
    """
    Тестирование случая, когда новый отпуск пересекается с существующим отпуском.
    """
    existing_vacation = sample_vacations[0]
    new_start_date = existing_vacation.start_date + timedelta(days=1)
    new_end_date = existing_vacation.end_date - timedelta(days=1)

    is_valid, error_message = check_vacation_overlap(
        new_start_date, new_end_date, sample_vacations
    )

    assert not is_valid
    assert error_message == ErrorMessages.OVERLAP_ERROR