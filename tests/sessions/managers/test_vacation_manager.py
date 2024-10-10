import pytest
from datetime import datetime

from src.models import UserData, VacationType, VacationStatus, Vacation, Limit
from src.sessions.managers.vacation_manager import VacationManager
from tests.data_fixtures.vacation_limits import vacation_limits
from tests.data_fixtures.vacation_schedule import vacation_schedule

@pytest.fixture
def user_data():
    return UserData(
        user_id="test_user",
        vacations=vacation_schedule,
        limits=vacation_limits
    )

@pytest.fixture
def vacation_manager(user_data):
    return VacationManager(user_data)

def test_create_new_vacation(vacation_manager):
    start_date = datetime.strptime("01.09.2025", "%d.%m.%Y")
    end_date = datetime.strptime("10.09.2025", "%d.%m.%Y")
    vacation = vacation_manager.create_new_vacation(
        vacation_type=VacationType.ANNUAL_PAID,
        start_date=start_date,
        end_date=end_date
    )
    assert vacation_manager.new_vacation == vacation
    assert vacation.start_date == start_date
    assert vacation.end_date == end_date
    assert vacation.vacation_type == VacationType.ANNUAL_PAID
    assert vacation.status == VacationStatus.PLANNED

def test_set_current_vacation_and_limit(vacation_manager):
    vacation_id = "1"
    vacation_manager.set_current_vacation_and_limit(vacation_id)
    assert vacation_manager.current_vacation.vacation_id == vacation_id
    assert vacation_manager.current_limit.vacation_type == VacationType.ANNUAL_PAID

def test_set_current_vacation_and_limit_not_found(vacation_manager, caplog):
    vacation_id = "non_existent_id"
    vacation_manager.set_current_vacation_and_limit(vacation_id)
    assert vacation_manager.current_vacation is None
    assert vacation_manager.current_limit is None
    assert f"Vacation {vacation_id} not found" in caplog.text

def test_get_new_vacation_dates(vacation_manager):
    # No new vacation yet
    assert vacation_manager.get_new_vacation_dates() is None

    # Create a new vacation
    start_date = datetime.strptime("01.09.2025", "%d.%m.%Y")
    end_date = datetime.strptime("10.09.2025", "%d.%m.%Y")
    vacation_manager.create_new_vacation(
        vacation_type=VacationType.UNPAID,
        start_date=start_date,
        end_date=end_date
    )
    dates = vacation_manager.get_new_vacation_dates()
    assert dates == (start_date, end_date)

def test_get_current_vacation_dates(vacation_manager):
    # No current vacation yet
    assert vacation_manager.get_current_vacation_dates() is None

    # Set current vacation
    vacation_manager.set_current_vacation_and_limit("2")
    dates = vacation_manager.get_current_vacation_dates()
    expected_start = datetime.strptime("01.03.2025", "%d.%m.%Y")
    expected_end = datetime.strptime("05.03.2025", "%d.%m.%Y")
    assert dates == (expected_start, expected_end)

def test_get_vacation_by_id(vacation_manager):
    vacation = vacation_manager.get_vacation_by_id("1")
    assert vacation is not None
    assert vacation.vacation_id == "1"

    # Test with non-existent ID
    vacation = vacation_manager.get_vacation_by_id("non_existent")
    assert vacation is None

def test_get_vacations_by_type(vacation_manager):
    vacations = vacation_manager.get_vacations_by_type(VacationType.ANNUAL_PAID)
    assert len(vacations) == 2
    for vacation in vacations:
        assert vacation.vacation_type == VacationType.ANNUAL_PAID

def test_get_limit_by_type(vacation_manager):
    limit = vacation_manager.get_limit_by_type(VacationType.UNPAID)
    assert limit is not None
    assert limit.available_days == 14

    # Test with non-existent vacation type
    limit = vacation_manager.get_limit_by_type("NON_EXISTENT_TYPE")
    assert limit is None

def test_reset_vacation_state(vacation_manager):
    # Set current and new vacations
    vacation_manager.set_current_vacation_and_limit("1")
    vacation_manager.create_new_vacation(
        vacation_type=VacationType.UNPAID,
        start_date=datetime.now(),
        end_date=datetime.now()
    )
    # Reset state
    vacation_manager.reset_vacation_state()
    assert vacation_manager.current_vacation is None
    assert vacation_manager.current_limit is None
    assert vacation_manager.new_vacation is None
