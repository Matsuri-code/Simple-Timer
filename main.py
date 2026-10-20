import sys
import tkinter as tk
from tkinter import messagebox

from updater import is_update_available, get_latest_release_url

try:
    # windows_toasts is Windows-only. On other platforms (or if the
    # package isn't installed) we fall back to a no-op implementation
    # so the app still runs; it simply won't show a native toast.
    if sys.platform == "win32":
        from windows_toasts import Toast, WindowsToaster
    else:
        raise ImportError("windows_toasts is only supported on Windows")

except ImportError:

    class Toast:
        def __init__(self):
            self.text_fields = []

    class WindowsToaster:
        def __init__(self, app_name):
            self.app_name = app_name

        def show_toast(self, toast):
            # Fallback: print to console instead of a native toast.
            message = " / ".join(toast.text_fields)
            print(f"[{self.app_name}] {message}")

from settings import SettingsManager
from themes import THEMES, get_theme
from audio import AudioPlayer
from version import APP_NAME, VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
from translations import t

MAX_TIMERS = 3


def resource_path(relative_path):
    """
    開発時（python main.py で実行）と、PyInstaller で exe 化した後の
    どちらでも、同梱したファイル（アイコンなど）を正しく見つけるための関数。
    PyInstaller は実行時、一時フォルダ（sys._MEIPASS）にファイルを展開する。
    """
    base_path = getattr(sys, "_MEIPASS", None)

    if base_path is None:
        import os
        base_path = os.path.dirname(os.path.abspath(__file__))

    import os
    return os.path.join(base_path, relative_path)


class TimerManager:
    """
    ① 複数のタイマーウィンドウを束ねる管理役。
    ② 最大3ウィンドウまでという制御をここで一元的に行う。
    ③ 言語・テーマなどの共有設定もここに持たせる。
    """

    def __init__(self):
        self.settings = SettingsManager.load_settings()
        self.settings.setdefault("language", "ja")

        self.windows = []      # 現在開いている TimerWindow のリスト
        self._next_slot = 1    # ウィンドウタイトル用の連番 ("Timer 1", "Timer 2"...)

    @property
    def language(self):
        return self.settings.get("language", "ja")

    # ---- ② 最大3ウィンドウ制御 -----------------------------------------

    def can_open_new(self):
        return len(self.windows) < MAX_TIMERS

    def take_slot(self):
        slot = self._next_slot
        self._next_slot += 1
        return slot

    def register(self, window):
        self.windows.append(window)

    def unregister(self, window):
        if window in self.windows:
            self.windows.remove(window)

        # 最後の1つが閉じたタイミングで設定を保存する
        if not self.windows:
            SettingsManager.save_settings(self.settings)

    # ---- 全ウィンドウへの一括反映 ----------------------------------------

    def refresh_language_all(self):
        for window in list(self.windows):
            window.refresh_texts()

    def refresh_theme_all(self):
        for window in list(self.windows):
            window.update_theme()


class TimerWindow:
    """
    ① 1つのタイマー/ストップウォッチを表す独立したウィンドウ。
    ④ 既存のメインタイマーの挙動（開始・一時停止・再開・停止・リセット・
       テーマ変更・アラーム設定）はそのまま維持する。
    ⑤ 終了時に自分専用の Windows 通知（トースト）を出す。
    """

    # ボタンを何列で並べるか（2列にすることで縦の必要スペースを半分近くに抑える）
    BUTTON_COLUMNS = 2

    def __init__(self, window, manager, is_main=False, slot=1):

        self.window = window
        self.manager = manager
        self.settings = manager.settings
        self.is_main = is_main
        self.slot = slot

        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        # 万一ボタン数が増えても隠れないよう、リサイズだけは許可しておく
        self.window.resizable(True, True)
        self.window.minsize(WINDOW_WIDTH, 400)

        # ウィンドウ左上の小さいアイコンを設定する。
        # アイコンファイルが見つからない環境でも起動自体は止めないよう try/except で囲む。
        try:
            self.window.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass

        self.audio = AudioPlayer()

        # ⑤ タイマーごとに区別できるよう、通知アプリ名にスロット番号を含める
        self.toaster = WindowsToaster(f"Simple Timer {self.slot}")

        self.timer_running = False
        self.stopwatch_running = False
        self.paused = False

        self.remaining = 0
        self.elapsed = 0

        self.after_id = None

        self.current_theme = self.settings["theme"]
        self.showing_placeholder = True

        self.apply_theme()

        self.title_label = tk.Label(
            self.window,
            text=APP_NAME,
            font=("Arial", 24, "bold")
        )

        self.title_label.pack(
            pady=(20, 10)
        )

        self.time_label = tk.Label(
            self.window,
            text="00:00",
            font=("Arial", 48, "bold")
        )

        self.time_label.pack(
            pady=10
        )

        self.entry = tk.Entry(
            self.window,
            width=18,
            justify="center",
            font=("Arial", 16)
        )

        self.entry.pack(
            pady=5
        )

        self.entry.insert(
            0,
            t("placeholder_seconds", self.manager.language)
        )

        self.entry.bind(
            "<FocusIn>",
            self.clear_placeholder
        )

        self.window.bind(
            "<Return>",
            self.start_timer_key
        )

        # ボタンをまとめて置く専用フレーム（2列グリッドで配置する）
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=(10, 15))

        # ③ ボタンは翻訳キーで保持しておき、言語切替時に一括で文言を差し替える
        self.buttons = {}
        self._button_count = 0

        self.create_button("btn_start_timer", self.start_timer)
        self.create_button("btn_start_stopwatch", self.start_stopwatch)
        self.create_button("btn_pause", self.pause)
        self.create_button("btn_resume", self.resume)
        self.create_button("btn_stop", self.stop)
        self.create_button("btn_reset", self.reset)
        self.create_button("btn_theme", self.change_theme)
        self.create_button("btn_alarm_select", self.select_alarm)
        self.create_button("btn_alarm_duration", self.set_alarm_duration)
        self.create_button("btn_new_timer", self.open_new_timer)
        self.create_button("btn_language", self.toggle_language)

        self.update_theme()
        self.update_window_title()

        self.manager.register(self)

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    # ------------------------------------------------------------------
    # 生成時の補助
    # ------------------------------------------------------------------

    def create_button(self, key, command):

        button = tk.Button(
            self.button_frame,
            text=t(key, self.manager.language),
            command=command,
            font=("Arial", 13, "bold"),
            width=18,
            height=2,
            relief="flat",
            bd=0
        )

        row = self._button_count // self.BUTTON_COLUMNS
        col = self._button_count % self.BUTTON_COLUMNS

        button.grid(
            row=row,
            column=col,
            padx=4,
            pady=3
        )

        self._button_count += 1

        self.buttons[key] = button

    def update_window_title(self):

        self.window.title(
            f"{APP_NAME} v{VERSION} - "
            f"{t('window_title', self.manager.language, n=self.slot)}"
        )

    # ------------------------------------------------------------------
    # ③ 日本語/英語切り替え
    # ------------------------------------------------------------------

    def toggle_language(self):

        current = self.settings.get("language", "ja")
        self.settings["language"] = "en" if current == "ja" else "ja"

        # 開いている全ウィンドウの文言を同時に更新する
        self.manager.refresh_language_all()

    def refresh_texts(self):

        lang = self.manager.language

        for key, button in self.buttons.items():
            button.config(text=t(key, lang))

        if self.showing_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, t("placeholder_seconds", lang))

        self.update_window_title()

    # ------------------------------------------------------------------
    # テーマ
    # ------------------------------------------------------------------

    def apply_theme(self):

        self.theme = get_theme(
            self.current_theme
        )

        self.window.configure(
            bg=self.theme["bg"]
        )

    def update_theme(self):

        self.apply_theme()

        self.title_label.config(
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        )

        self.time_label.config(
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        )

        self.entry.config(
            bg="white",
            fg="black"
        )

        self.button_frame.config(
            bg=self.theme["bg"]
        )

        for button in self.buttons.values():

            button.config(
                bg=self.theme["button_bg"],
                fg=self.theme["button_fg"],
                activebackground=self.theme["button_bg"],
                activeforeground=self.theme["button_fg"]
            )

    def change_theme(self):

        names = list(
            THEMES.keys()
        )

        index = names.index(
            self.current_theme
        )

        index += 1

        if index >= len(names):
            index = 0

        self.current_theme = names[index]

        self.settings["theme"] = (
            self.current_theme
        )

        # 開いている全ウィンドウのテーマも揃える
        for tw in self.manager.windows:
            tw.current_theme = self.current_theme

        self.manager.refresh_theme_all()

        messagebox.showinfo(
            t("theme_changed_title", self.manager.language),
            t("theme_changed_msg", self.manager.language, theme=self.current_theme)
        )

    # ------------------------------------------------------------------
    # 入力欄まわり
    # ------------------------------------------------------------------

    def clear_placeholder(
        self,
        event
    ):

        if self.showing_placeholder:

            self.entry.delete(
                0,
                tk.END
            )

            self.showing_placeholder = False

    def start_timer_key(
        self,
        event
    ):

        self.start_timer()

    # ------------------------------------------------------------------
    # ④ タイマー/ストップウォッチ本体（既存ロジックを維持）
    # ------------------------------------------------------------------

    def start_timer(self):

        try:

            self.remaining = int(
                self.entry.get()
            )

            if self.remaining <= 0:
                raise ValueError

        except Exception:

            messagebox.showerror(
                t("error_title", self.manager.language),
                t("error_seconds", self.manager.language)
            )

            return

        self.stop()

        self.timer_running = True
        self.stopwatch_running = False
        self.paused = False

        self.update_timer()

    def update_timer(self):

        if not self.timer_running:
            return

        if not self.paused:

            mins = self.remaining // 60
            secs = self.remaining % 60

            self.time_label.config(
                text=f"{mins:02}:{secs:02}"
            )

            if self.remaining <= 0:

                self.timer_running = False

                self.audio.current_file = (
                    self.settings["alarm_file"]
                )

                self.audio.play(
                    self.settings["alarm_duration"]
                )

                self.notify_finished()

                messagebox.showinfo(
                    t("finished_title", self.manager.language),
                    t("finished_msg", self.manager.language)
                )

                return

            self.remaining -= 1

        self.after_id = self.window.after(
            1000,
            self.update_timer
        )

    def start_stopwatch(self):

        self.stop()

        self.elapsed = 0
        self.stopwatch_running = True
        self.paused = False

        self.update_stopwatch()

    def update_stopwatch(self):

        if not self.stopwatch_running:
            return

        if not self.paused:

            mins = self.elapsed // 60
            secs = self.elapsed % 60

            self.time_label.config(
                text=f"{mins:02}:{secs:02}"
            )

            self.elapsed += 1

        self.after_id = self.window.after(
            1000,
            self.update_stopwatch
        )

    def pause(self):

        self.paused = True

    def resume(self):

        self.paused = False

    def stop(self):

        self.timer_running = False
        self.stopwatch_running = False
        self.paused = False

        if self.after_id:

            self.window.after_cancel(
                self.after_id
            )

            self.after_id = None

    def reset(self):

        self.stop()

        self.remaining = 0
        self.elapsed = 0

        self.time_label.config(
            text="00:00"
        )

    # ------------------------------------------------------------------
    # ⑤ Windows通知
    # ------------------------------------------------------------------

    def notify_finished(self):

        lang = self.manager.language

        toast = Toast()

        toast.text_fields = [
            t("toast_title", lang),
            t("toast_msg", lang) + f"  ({t('window_title', lang, n=self.slot)})"
        ]

        self.toaster.show_toast(toast)

    # ------------------------------------------------------------------
    # アラーム設定
    # ------------------------------------------------------------------

    def select_alarm(self):

        file_path = self.audio.select_file()

        if file_path:

            self.settings["alarm_file"] = file_path

            messagebox.showinfo(
                t("alarm_title", self.manager.language),
                t("alarm_set_msg", self.manager.language)
            )

    def set_alarm_duration(self):

        lang = self.manager.language

        window = tk.Toplevel(self.window)

        window.title(t("alarm_duration_title", lang))
        window.geometry("250x120")
        window.resizable(False, False)

        tk.Label(
            window,
            text=t("alarm_duration_hint", lang)
        ).pack(pady=10)

        entry = tk.Entry(
            window,
            justify="center"
        )

        entry.pack()

        entry.insert(
            0,
            str(
                self.settings["alarm_duration"]
            )
        )

        def save():

            try:

                value = int(entry.get())

                if not 5 <= value <= 30:
                    raise ValueError

                self.settings["alarm_duration"] = value

                window.destroy()

            except Exception:

                messagebox.showerror(
                    t("duration_error_title", lang),
                    t("duration_error_msg", lang)
                )

        tk.Button(
            window,
            text=t("save", lang),
            command=save
        ).pack(
            pady=10
        )

    # ------------------------------------------------------------------
    # ② 新規ウィンドウ（最大3つまで）
    # ------------------------------------------------------------------

    def open_new_timer(self):

        if not self.manager.can_open_new():

            messagebox.showwarning(
                t("max_timers_title", self.manager.language),
                t("max_timers_msg", self.manager.language)
            )

            return

        new_toplevel = tk.Toplevel(self.window)
        slot = self.manager.take_slot()

        TimerWindow(
            new_toplevel,
            self.manager,
            is_main=False,
            slot=slot
        )

    # ------------------------------------------------------------------
    # 終了処理
    # ------------------------------------------------------------------

    def on_close(self):

        self.stop()

        self.manager.unregister(self)

        # メインウィンドウを閉じると、子であるToplevelも道連れで閉じる
        self.window.destroy()


def main():

    root = tk.Tk()

    update_available, latest = is_update_available()

    manager = TimerManager()
    lang = manager.language

    if update_available:

        result = messagebox.askyesno(
            t("update_title", lang),
            t("update_msg", lang, latest=latest)
        )

        if result:

            import webbrowser

            url = get_latest_release_url()

            if url:
                webbrowser.open(url)

    slot = manager.take_slot()

    # ④ 既存の「メインタイマー」はこれまでどおり、ルートウィンドウ上に生成される
    main_window = TimerWindow(
        root,
        manager,
        is_main=True,
        slot=slot
    )

    root.mainloop()


if __name__ == "__main__":
    main()
