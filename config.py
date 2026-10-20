"""App-wide file paths (settings location, etc.)."""

import os
import sys

from version import APP_NAME


def _get_app_data_dir():

    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.join(
            os.path.expanduser("~"), "Library", "Application Support"
        )
    else:
        base = os.environ.get(
            "XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config")
        )

    app_dir = os.path.join(base, APP_NAME)
    os.makedirs(app_dir, exist_ok=True)

    return app_dir


SETTINGS_FILE = os.path.join(_get_app_data_dir(), "settings.json")
