from typing import Tuple

from src.constants import CALLBACK_DATA_SEPARATOR


def parse_callback_data(callback_data: str) -> Tuple[str, str]:
    """
    Split callback_data into prefix and value.

    Args:
        callback_data (str): The callbackData string to split.

    Returns:
        Tuple[str, str]: A tuple containing the prefix and value.
    """
    if CALLBACK_DATA_SEPARATOR in callback_data:
        prefix, value = callback_data.split(CALLBACK_DATA_SEPARATOR, 1)
        return prefix, value
    return callback_data, ""
