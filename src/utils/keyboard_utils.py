from typing import List, Dict, Any

from src.buttons.bot_button import BotButton
from src.constants import CALLBACK_DATA_SEPARATOR
from src.models import Vacation
from src.styles.button_style import ButtonStyle


def create_keyboard(
    buttons: List[BotButton],
) -> List[List[Dict[str, Any]]]:
    """
    Create a keyboard based on a list of buttons
    Args:
        buttons (List[BotButton]): A list of buttons to create a keyboard.
    Returns:
        List[List[Dict[str, Any]]]: A generated keyboard layout.

    Raises:
        ValueError: If the buttons list is empty.
    """
    if not buttons:
        raise ValueError("The 'buttons' list cannot be empty.")

    return [
        [{
            "text": button.text,
            "callbackData": button.callback_data,
            "style": button.style
        }]
        for button in buttons
    ]


def create_vacation_keyboard(
    vacations: List[Vacation],
    callback_prefix: str,
    button_style: ButtonStyle = ButtonStyle.PRIMARY
) -> List[List[Dict[str, str]]]:
    """
    Create a keyboard based on a list of buttons with the specified callback prefix and button style.

    Args:
        vacations (List[Vacation]): List of vacations.
        callback_prefix (str): Prefix for callback data.
        button_style (ButtonStyle, optional): Style of the button for the interface. Defaults to ButtonStyle.PRIMARY.

    Returns:
        List[List[Dict[str, str]]]: List of buttons for the bot interface.
    """
    keyboard = []

    for idx, vacation in enumerate(vacations, 1):
        callback_data = f"{callback_prefix}{CALLBACK_DATA_SEPARATOR}{vacation.vacation_id}"
        button_text = (
            f"{idx}. С {vacation.start_date.strftime('%d.%m.%Y')} по {vacation.end_date.strftime('%d.%m.%Y')}, "
            f"тип: {vacation.vacation_type}, статус: {vacation.status}"
        )

        button = {
            "text": button_text,
            "callbackData": callback_data,
            "style": button_style.value
        }

        keyboard.append([button])

    return keyboard
