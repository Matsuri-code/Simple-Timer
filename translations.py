"""Simple translation helper for Japanese / English UI text."""

LANGUAGES = ["ja", "en"]

TRANSLATIONS = {
    "placeholder_seconds": {"ja": "秒数を入力", "en": "Enter seconds"},

    "btn_start_timer": {"ja": "▶ タイマー開始", "en": "▶ Start Timer"},
    "btn_start_stopwatch": {"ja": "⏱ ストップウォッチ", "en": "⏱ Stopwatch"},
    "btn_pause": {"ja": "⏸ 一時停止", "en": "⏸ Pause"},
    "btn_resume": {"ja": "▶ 再開", "en": "▶ Resume"},
    "btn_stop": {"ja": "⛔ 停止", "en": "⛔ Stop"},
    "btn_reset": {"ja": "🔄 リセット", "en": "🔄 Reset"},
    "btn_theme": {"ja": "🎨 テーマ変更", "en": "🎨 Change Theme"},
    "btn_alarm_select": {"ja": "🔔 アラーム音選択", "en": "🔔 Select Alarm Sound"},
    "btn_alarm_duration": {"ja": "⏳ アラーム時間設定", "en": "⏳ Set Alarm Duration"},
    "btn_new_timer": {"ja": "➕ 新しいタイマー", "en": "➕ New Timer"},
    "btn_language": {"ja": "🌐 English", "en": "🌐 日本語"},

    "error_title": {"ja": "入力エラー", "en": "Input Error"},
    "error_seconds": {
        "ja": "1以上の秒数を入力してください。",
        "en": "Please enter a number of seconds greater than 0.",
    },

    "finished_title": {"ja": "終了", "en": "Finished"},
    "finished_msg": {"ja": "時間になりました。", "en": "Time's up."},

    "toast_title": {"ja": "タイマー終了", "en": "Timer Finished"},
    "toast_msg": {
        "ja": "設定した時間になりました。",
        "en": "The set time has elapsed.",
    },

    "theme_changed_title": {"ja": "テーマ変更", "en": "Theme Changed"},
    "theme_changed_msg": {"ja": "{theme} に変更しました。", "en": "Changed to {theme}."},

    "alarm_title": {"ja": "アラーム", "en": "Alarm"},
    "alarm_set_msg": {
        "ja": "アラーム音を設定しました。",
        "en": "Alarm sound has been set.",
    },

    "alarm_duration_title": {"ja": "アラーム時間", "en": "Alarm Duration"},
    "alarm_duration_hint": {"ja": "5～30秒", "en": "5-30 seconds"},
    "save": {"ja": "保存", "en": "Save"},
    "duration_error_title": {"ja": "エラー", "en": "Error"},
    "duration_error_msg": {
        "ja": "5～30の数字を入力してください。",
        "en": "Please enter a number between 5 and 30.",
    },

    "update_title": {"ja": "アップデート", "en": "Update Available"},
    "update_msg": {
        "ja": "新しいバージョン {latest} が公開されています。\n\nGitHubの更新ページを開きますか？",
        "en": "A new version {latest} is available.\n\nWould you like to open the GitHub release page?",
    },

    "max_timers_title": {"ja": "上限", "en": "Limit Reached"},
    "max_timers_msg": {
        "ja": "タイマーは最大3つまで起動できます。",
        "en": "You can open up to 3 timers at once.",
    },

    "window_title": {"ja": "タイマー {n}", "en": "Timer {n}"},
}


def t(key, lang="ja", **kwargs):
    """Return the translated string for `key` in `lang`, formatted with kwargs."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("ja", key))
    if kwargs:
        text = text.format(**kwargs)
    return text
