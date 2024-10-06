import json
import logging
from pathlib import Path
from typing import Union, Dict, Any, List

#TODO: Should be refactored. Sure to use base_path everywhere.
class TextLoader:
    """
    A class for loading and accessing textual resources.

    Attributes:
        base_path (Path): The base path to the text files.
        texts (Dict[str, Any]): The loaded text data.
        logger (logging.Logger): Logger for the class.
    """

    def __init__(self, base_path: Union[str, Path] = 'texts') -> None:
        """
        Initializes the TextLoader.

        Args:
            base_path (Union[str, Path]): The relative path to the directory containing text files.
        """
        self.base_path: Path = Path(base_path)
        self.texts: Dict[str, Any] = {}
        self.logger: logging.Logger = logging.getLogger(__name__)
        self._load_texts()

    def _load_texts(self) -> None:
        """Loads text files into the texts dictionary."""
        for file_path in self.base_path.rglob('*.json'):
            if not file_path.is_file():
                continue

            relative_path = file_path.relative_to(self.base_path)
            keys = relative_path.with_suffix('').parts

            # Handle files where the filename matches the parent directory (e.g., buttons/buttons.json)
            if len(keys) >= 2 and keys[-1] == keys[-2]:
                keys = keys[:-1]

            try:
                with file_path.open('r', encoding='utf-8') as f:
                    content = json.load(f)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to decode JSON from {file_path}: {e}")
                continue

            self._merge_content(keys, content)

    def _merge_content(self, keys: List[str], content: Any) -> None:
        """Recursively merges content into the texts dictionary."""
        current_level = self.texts
        for key in keys[:-1]:
            current_level = current_level.setdefault(key, {})
        last_key = keys[-1]

        if last_key in current_level:
            existing_content = current_level[last_key]
            if isinstance(existing_content, dict) and isinstance(content, dict):
                self._deep_update(existing_content, content)
            else:
                self.logger.warning(f"Overwriting key '{last_key}' in '{'.'.join(keys[:-1])}'")
                current_level[last_key] = content
        else:
            current_level[last_key] = content

    def _deep_update(self, dest: Dict[str, Any], src: Dict[str, Any]) -> None:
        """Recursively updates nested dictionaries."""
        for key, value in src.items():
            if key in dest and isinstance(dest[key], dict) and isinstance(value, dict):
                self._deep_update(dest[key], value)
            else:
                dest[key] = value

    def get(self, *keys: str, **kwargs: Any) -> str:
        """
        Retrieves text by the given keys.

        Args:
            *keys (str): A sequence of keys to access the desired text.
            **kwargs: Additional arguments for string formatting.

        Returns:
            str: The requested text formatted with kwargs if provided.

        If the text is not found, returns a string like "[category.section.key]"
        and logs a warning.
        """
        missing_key = f"[{'.'.join(keys)}]"
        value = self._get_value_by_keys(keys)
        if value is None:
            self.logger.warning(f"Missing text for {missing_key}")
            return missing_key

        if isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError as e:
                self.logger.error(f"Missing formatting key {e} in text for {missing_key}")
                return value
        else:
            self.logger.warning(f"Text at {'.'.join(keys)} is not a string.")
            return missing_key

    def _get_value_by_keys(self, keys: List[str]) -> Any:
        """Retrieves a value from the texts dictionary by a list of keys."""
        current_level = self.texts
        for key in keys:
            if isinstance(current_level, dict) and key in current_level:
                current_level = current_level[key]
            else:
                return None
        return current_level