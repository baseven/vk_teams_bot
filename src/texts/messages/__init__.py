from types import SimpleNamespace

from src.utils.text_loader import text_loader

messages = SimpleNamespace(**{
    section: SimpleNamespace(**texts)
    for section, texts in text_loader.texts['messages'].items()
})
