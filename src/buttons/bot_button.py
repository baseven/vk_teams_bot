from dataclasses import dataclass

from src.styles.button_style import ButtonStyle


@dataclass(frozen=True)
class BotButton:
    callback_data: str
    text: str = ""
    style: str = ButtonStyle.PRIMARY.value
