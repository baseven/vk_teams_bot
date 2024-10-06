import json
import logging

import pytest

from src.utils.text_loader import TextLoader


#TODO: Should be refactored after TextLoader is refactored
@pytest.fixture
def text_loader(tmp_path):
    """
    Fixture to create a TextLoader instance with temporary text files.
    """
    texts_dir = tmp_path / "texts"
    texts_dir.mkdir()

    # Create 'buttons/buttons.json'
    buttons_dir = texts_dir / "buttons"
    buttons_dir.mkdir()

    buttons_content = {
        "common": {
            "BACK_TO_MAIN_MENU": "Вернуться в главное меню"
        },
        "main_menu": {
            "ANNUAL_VACATION_MENU": "Оформить ежегодный отпуск",
            "UNPAID_VACATION_MENU": "Оформить отпуск без оплаты",
            "LIMITS_AND_VACATIONS_MENU": "Посмотреть лимиты и график отпусков",
            "RESCHEDULE_VACATION_MENU": "Перенести отпуск",
            "CANCEL_VACATION_MENU": "Отменить отпуск"
        },
        "annual_vacation": {
            "HANDLE_ANNUAL_VACATION": "",
            "CREATE_ANNUAL_VACATION": "Другие даты",
            "CONFIRM_ANNUAL_VACATION": "Оформить",
            "BACK_TO_MAIN_MENU": "Вернуться в главное меню"
        }
        # Add other sections if necessary
    }
    buttons_json = buttons_dir / "buttons.json"
    buttons_json.write_text(json.dumps(buttons_content, ensure_ascii=False), encoding='utf-8')

    # Create 'messages/messages.json'
    messages_dir = texts_dir / "messages"
    messages_dir.mkdir()

    messages_content = {
        "annual_vacation": {
            "HANDLE_ANNUAL_VACATION": "Оформить отпуск с {start_date} по {end_date}?"
        }
    }
    messages_json = messages_dir / "messages.json"
    messages_json.write_text(json.dumps(messages_content, ensure_ascii=False), encoding='utf-8')

    # Create 'errors.json'
    errors_json = texts_dir / "errors.json"
    errors_content = {
        "INVALID_DATE": "Неверный формат даты. Пожалуйста, используйте ДД.ММ.ГГГГ."
    }
    errors_json.write_text(json.dumps(errors_content, ensure_ascii=False), encoding='utf-8')

    # Return a TextLoader instance
    return TextLoader(base_path=texts_dir)


def test_load_texts(text_loader):
    """Test that texts are loaded correctly."""
    assert 'buttons' in text_loader.texts
    assert 'common' in text_loader.texts['buttons']
    assert 'main_menu' in text_loader.texts['buttons']
    assert 'ANNUAL_VACATION_MENU' in text_loader.texts['buttons']['main_menu']


def test_get_existing_text(text_loader):
    """Test retrieving an existing text."""
    text = text_loader.get('buttons', 'main_menu', 'ANNUAL_VACATION_MENU')
    assert text == "Оформить ежегодный отпуск"


def test_get_missing_text(text_loader, caplog):
    """Test retrieving a missing text."""
    with caplog.at_level(logging.WARNING):
        text = text_loader.get('buttons', 'main_menu', 'NON_EXISTENT_KEY')
    assert text == "[buttons.main_menu.NON_EXISTENT_KEY]"
    assert "Missing text for [buttons.main_menu.NON_EXISTENT_KEY]" in caplog.text


def test_text_formatting(text_loader):
    """Test text formatting with kwargs."""
    text = text_loader.get(
        'messages', 'annual_vacation', 'HANDLE_ANNUAL_VACATION',
        start_date="01.01.2023", end_date="10.01.2023"
    )
    assert text == "Оформить отпуск с 01.01.2023 по 10.01.2023?"


def test_get_text_with_non_string_value(text_loader, caplog):
    """Test handling of non-string values."""
    # Change the text to a dictionary instead of a string
    text_loader.texts['buttons']['main_menu']['INVALID_ENTRY'] = {"key": "value"}
    with caplog.at_level(logging.WARNING):
        text = text_loader.get('buttons', 'main_menu', 'INVALID_ENTRY')
    assert text == "[buttons.main_menu.INVALID_ENTRY]"
    assert "Text at buttons.main_menu.INVALID_ENTRY is not a string." in caplog.text


def test_json_decode_error(tmp_path, caplog):
    """Test handling of invalid JSON files."""
    texts_dir = tmp_path / "texts"
    texts_dir.mkdir()

    invalid_json_file = texts_dir / "invalid.json"
    invalid_json_file.write_text("{invalid_json: true", encoding='utf-8')  # Invalid JSON

    with caplog.at_level(logging.ERROR):
        text_loader = TextLoader(base_path=texts_dir)
    assert "Failed to decode JSON from" in caplog.text