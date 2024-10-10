import pytest
from unittest.mock import MagicMock

from src.sessions.user_session import UserSession
from src.models import UserData
from src.services import UserDataDatabaseService
from tests.data_fixtures.vacation_limits import vacation_limits
from tests.data_fixtures.vacation_schedule import vacation_schedule

@pytest.fixture
def mock_database_service():
    service = MagicMock(spec=UserDataDatabaseService)
    service.get_user_data.return_value = None
    return service

@pytest.fixture
def user_session(mock_database_service):
    return UserSession(user_id="test_user", database_service=mock_database_service)

def test_user_session_initialization(user_session, mock_database_service):
    # Test that user_data is initialized when not found in the database
    assert user_session.user_data.user_id == "test_user"
    assert user_session.user_data.vacations == vacation_schedule
    assert user_session.user_data.limits == vacation_limits
    mock_database_service.save_user_data.assert_called_once()

def test_user_session_properties(user_session):
    # Test getter and setter for last_bot_message_id
    user_session.last_bot_message_id = "12345"
    assert user_session.last_bot_message_id == "12345"

    # Test getter and setter for state
    user_session.state = "new_state"
    assert user_session.state == "new_state"

def test_user_session_save_session(user_session, mock_database_service):
    user_session.state_machine.to_annual_vacation_menu()
    user_session.save_session()
    # Ensure that user_data.state is updated
    assert user_session.user_data.state == "annual_vacation_menu"
    # Verify that save_user_data was called with updated user_data
    mock_database_service.save_user_data.assert_called_with(user_session.user_data)
