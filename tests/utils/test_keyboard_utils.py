import pytest

from src.constants import CALLBACK_DATA_SEPARATOR, DATE_FORMAT
from src.styles.button_style import ButtonStyle
from src.utils.keyboard_utils import create_keyboard, create_vacation_keyboard


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
    Test create_keyboard with empty buttons list.
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
            f"{idx}. С {vacation.start_date.strftime(DATE_FORMAT)} по {vacation.end_date.strftime(DATE_FORMAT)}, "
            f"тип: {vacation.vacation_type}, статус: {vacation.status}"
        )
        assert button['text'] == expected_text
        assert button['callbackData'] == expected_callback_data
        assert button['style'] == ButtonStyle.PRIMARY.value
