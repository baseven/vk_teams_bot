from dataclasses import dataclass

@dataclass(frozen=True)
class BotAction:
    callback_data: str
    text: str = ""
