from types import SimpleNamespace

from src.utils.text_loader import text_loader

buttons = SimpleNamespace(**{
    section: SimpleNamespace(**texts)
    for section, texts in text_loader.texts['buttons'].items()
})
