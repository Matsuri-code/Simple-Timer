import requests

from version import GITHUB_REPOSITORY, VERSION


def get_latest_release():
    """GitHub Releasesの最新情報を取得"""

    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/releases/latest"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return None


def is_update_available():
    """新しいバージョンがあるか確認"""

    release = get_latest_release()

    if release is None:
        return False, None

    latest = release["tag_name"].lstrip("v")
    current = VERSION.lstrip("v")

    latest_parts = [int(x) for x in latest.split(".")]
    current_parts = [int(x) for x in current.split(".")]

    while len(latest_parts) < 3:
        latest_parts.append(0)

    while len(current_parts) < 3:
        current_parts.append(0)

    return latest_parts > current_parts, latest


def get_latest_release_url():
    """最新ReleaseのページURLを取得"""

    release = get_latest_release()

    if release is None:
        return None

    return release.get("html_url")