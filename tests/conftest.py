import pytest
from src.buttons.bot_button import BotButton
from tests.data_fixtures.vacation_limits import vacation_limits
from tests.data_fixtures.vacation_schedule import vacation_schedule


@pytest.fixture
def sample_actions():
    return [
        BotButton(text="Action 1", callback_data="callback1"),
        BotButton(text="Action 2", callback_data="callback2")
    ]

@pytest.fixture
def sample_vacations():
    return vacation_schedule

@pytest.fixture
def sample_limits():
    return vacation_limits
