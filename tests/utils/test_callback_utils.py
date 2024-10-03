from src.constants import CALLBACK_DATA_SEPARATOR
from src.utils.callback_utils import parse_callback_data


def test_parse_callback_data():
    """
    Test the parse_callback_data function.
    """
    callback_data = f"prefix{CALLBACK_DATA_SEPARATOR}value"
    prefix, value = parse_callback_data(callback_data)
    assert prefix == "prefix"
    assert value == "value"

    callback_data = "noprefix"
    prefix, value = parse_callback_data(callback_data)
    assert prefix == "noprefix"
    assert value == ""
