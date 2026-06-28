import tkinter as tk
from tkinter import messagebox

from settings import SettingsManager
from themes import THEMES, get_theme
from audio import AudioPlayer
from version import APP_NAME, VERSION
class SimpleTimerApp:

    def __init__(self, root):

        self.root = root

        self.settings = SettingsManager.load_settings()

        self.root.title(
            f"{APP_NAME}  v{VERSION}"
        )

        self.root.geometry("420x700")
        self.root.resizable(False, False)

        self.audio = AudioPlayer()

        self.timer_running = False
        self.stopwatch_running = False
        self.paused = False

        self.remaining = 0
        self.elapsed = 0

        self.after_id = None

        self.current_theme = self.settings["theme"]

        self.apply_theme()

        self.title_label = tk.Label(
            self.root,
            text=APP_NAME,
            font=("Arial", 24, "bold")
        )

        self.title_label.pack(
            pady=(20, 10)
        )

        self.time_label = tk.Label(
            self.root,
            text="00:00",
            font=("Arial", 48, "bold")
        )

        self.time_label.pack(
            pady=10
        )

        self.entry = tk.Entry(
            self.root,
            width=18,
            justify="center",
            font=("Arial", 16)
        )

        self.entry.pack(
            pady=5
        )

        self.entry.insert(
            0,
            "秒数を入力"
        )

        self.entry.bind(
            "<FocusIn>",
            self.clear_placeholder
        )

        self.root.bind(
            "<Return>",
            self.start_timer_key
        )

        self.buttons = []
        self.create_button(
            "▶ タイマー開始",
            self.start_timer
        )

        self.create_button(
            "⏱ ストップウォッチ",
            self.start_stopwatch
        )

        self.create_button(
            "⏸ 一時停止",
            self.pause
        )

        self.create_button(
            "▶ 再開",
            self.resume
        )

        self.create_button(
            "⛔ 停止",
            self.stop
        )

        self.create_button(
            "🔄 リセット",
            self.reset
        )

        self.create_button(
            "🎨 テーマ変更",
            self.change_theme
        )

        self.create_button(
            "🔔 アラーム音選択",
            self.select_alarm
        )

        self.create_button(
            "⏳ アラーム時間設定",
            self.set_alarm_duration
        )

        self.update_theme()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
                )

    def create_button(
        self,
        text,
        command
    ):

        button = tk.Button(
            self.root,
            text=text,
            command=command,
            font=("Arial", 13, "bold"),
            width=18,
            height=2,
            relief="flat",
            bd=0
        )

        button.pack(
            pady=3
        )

        self.buttons.append(button)

    def apply_theme(self):

        self.theme = get_theme(
            self.current_theme
        )

        self.root.configure(
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

        for button in self.buttons:

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

        self.update_theme()

        messagebox.showinfo(
            "テーマ変更",
            f"{self.current_theme} に変更しました。"
        )


    def clear_placeholder(
        self,
        event
    ):

        if self.entry.get() == "秒数を入力":

            self.entry.delete(
                0,
                tk.END
            )


    def start_timer_key(
        self,
        event
    ):

        self.start_timer()


    def start_timer(self):

        try:

            self.remaining = int(
                self.entry.get()
            )

            if self.remaining <= 0:
                raise ValueError

        except:

            messagebox.showerror(
                "入力エラー",
                "1以上の秒数を入力してください。"
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
                    self.settings[
                        "alarm_duration"
                    ]
                )

                messagebox.showinfo(
                    "終了",
                    "時間になりました。"
                )

                return

            self.remaining -= 1

        self.after_id = self.root.after(
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

        self.after_id = self.root.after(
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

            self.root.after_cancel(
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

    def select_alarm(self):

        file_path = self.audio.select_file()

        if file_path:

            self.settings["alarm_file"] = file_path

            messagebox.showinfo(
                "アラーム",
                "アラーム音を設定しました。"
            )

    def set_alarm_duration(self):

        window = tk.Toplevel(self.root)

        window.title("アラーム時間")
        window.geometry("250x120")
        window.resizable(False, False)

        tk.Label(
            window,
            text="5～30秒"
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

                self.settings[
                    "alarm_duration"
                ] = value

                window.destroy()

            except:

                messagebox.showerror(
                    "エラー",
                    "5～30の数字を入力してください。"
                )

        tk.Button(
            window,
            text="保存",
            command=save
        ).pack(
            pady=10
        )


    def on_close(self):

        self.stop()

        SettingsManager.save_settings(
            self.settings
        )

        self.root.destroy()


def main():

    root = tk.Tk()

    app = SimpleTimerApp(root)

    root.mainloop()


if __name__ == "__main__":

    main()