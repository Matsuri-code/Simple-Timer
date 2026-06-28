import json
import os

from config import SETTINGS_FILE


DEFAULT_SETTINGS = {
    "theme": "Light",
    "alarm_file": "",
    "alarm_duration": 10
}


class SettingsManager:

    @staticmethod
    def load_settings():

        if not os.path.exists(SETTINGS_FILE):
            return DEFAULT_SETTINGS.copy()

        try:
            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            settings = DEFAULT_SETTINGS.copy()
            settings.update(data)

            return settings

        except Exception:
            return DEFAULT_SETTINGS.copy()

    @staticmethod
    def save_settings(settings):

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                settings,
                f,
                indent=4,
                ensure_ascii=False
            )