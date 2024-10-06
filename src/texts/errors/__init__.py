from types import SimpleNamespace

from src.utils.text_loader import text_loader

errors = SimpleNamespace(**text_loader.texts['errors'])
