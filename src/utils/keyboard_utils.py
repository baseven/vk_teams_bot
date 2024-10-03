from typing import List, Dict, Any

from src.actions.bot_action import BotAction
from src.constants import CALLBACK_DATA_SEPARATOR
from src.models import Vacation
from src.styles import ButtonStyle



def create_keyboard(
    actions: List[BotAction],
    button_style: ButtonStyle = ButtonStyle.PRIMARY
) -> List[List[Dict[str, Any]]]:
    """
    Create a keyboard layout based on a list of actions and a button style.

    Args:
        actions (List[BotAction]): A list of actions to create buttons for.
        button_style (ButtonStyle, optional): The style to apply to each button. Defaults to ButtonStyle.PRIMARY.

    Returns:
        List[List[Dict[str, Any]]]: A generated keyboard layout.

    Raises:
        ValueError: If the actions list is empty.
    """
    if not actions:
        raise ValueError("The 'actions' list cannot be empty.")

    return [
        [{
            "text": action.text,
            "callbackData": action.callback_data,
            "style": button_style.value
        }]
        for action in actions
    ]


def create_vacation_keyboard(
    vacations: List[Vacation],
    callback_prefix: str,
    button_style: ButtonStyle = ButtonStyle.PRIMARY
) -> List[List[Dict[str, str]]]:
    """
    Create buttons for vacations with the specified callback prefix and button style.

    Args:
        vacations (List[Vacation]): List of vacations.
        callback_prefix (str): Prefix for callback data.
        button_style (ButtonStyle, optional): Style of the button for the interface. Defaults to ButtonStyle.PRIMARY.

    Returns:
        List[List[Dict[str, str]]]: List of buttons for the bot interface.
    """
    buttons = []

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

        buttons.append([button])

    return buttons
