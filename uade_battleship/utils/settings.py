from enum import Enum
from typing import Any
from .file_storage import FileStorage
import json


class SettingsKey(Enum):
    VOLUME = "volume"


class Settings:
    SETTINGS_FILE = "settings.json"
    _settings = {}
    _defaults = {SettingsKey.VOLUME: 0.5}

    @classmethod
    def _load_settings(cls):
        try:
            content = FileStorage.read_file(cls.SETTINGS_FILE)
            if content:
                cls._settings = json.loads(content)
            else:
                cls.set_and_save_default()
        except Exception as e:
            print(f"Error loading settings: {e}")
            cls.set_and_save_default()

    @classmethod
    def set_and_save_default(cls):
        cls._settings = {key.value: value for key, value in cls._defaults.items()}
        cls._save_settings()

    @classmethod
    def _save_settings(cls):
        try:
            FileStorage.write_file(cls.SETTINGS_FILE, json.dumps(cls._settings))
        except Exception as e:
            print(f"Error saving settings: {e}")

    @classmethod
    def get(cls, key: SettingsKey) -> Any:
        """
        Get a setting value by key. Returns default value if not set.
        """
        if not cls._settings:
            cls._load_settings()
        return cls._settings.get(key.value, cls._defaults.get(key))

    @classmethod
    def set(cls, key: SettingsKey, value: Any) -> None:
        """
        Set a setting value and save to storage.
        """
        if not cls._settings:
            cls._load_settings()
        cls._settings[key.value] = value
        cls._save_settings()
