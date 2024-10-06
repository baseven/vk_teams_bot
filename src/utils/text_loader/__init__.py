from pathlib import Path

from .text_loader import TextLoader


base_path = Path(__file__).parent.parent.parent / 'texts'

text_loader = TextLoader(base_path=base_path)

__all__ = ['TextLoader', 'text_loader']
