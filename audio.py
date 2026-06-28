import os
import tkinter as tk
from tkinter import filedialog, messagebox

import pygame


class AudioPlayer:

    def __init__(self):

        pygame.mixer.init()

        self.current_file = ""
        self.is_playing = False
        self.volume = 1.0

    def select_file(self):

        file_path = filedialog.askopenfilename(
            title="アラーム音を選択",
            filetypes=[
                ("音声ファイル", "*.mp3 *.wav"),
                ("MP3", "*.mp3"),
                ("WAV", "*.wav"),
                ("すべて", "*.*")
            ]
        )

        if file_path:
            self.current_file = file_path

        return self.current_file

    def play(self, duration=10):

        if not self.current_file:

            messagebox.showwarning(
                "アラーム",
                "アラーム音が設定されていません。"
            )
            return

        if not os.path.exists(self.current_file):

            messagebox.showerror(
                "エラー",
                "音声ファイルが見つかりません。"
            )
            return

        try:

            pygame.mixer.music.load(
                self.current_file
            )

            pygame.mixer.music.set_volume(
                self.volume
            )

            pygame.mixer.music.play()

            self.is_playing = True

            duration = max(
                5,
                min(30, duration)
            )

            root = tk._default_root

            if root:

                root.after(
                    duration * 1000,
                    self.stop
                )

        except Exception as e:

            messagebox.showerror(
                "再生エラー",
                str(e)
            )

    def stop(self):

        pygame.mixer.music.stop()

        self.is_playing = False

    def set_volume(self, volume):

        volume = max(
            0,
            min(1, volume)
        )

        self.volume = volume

        pygame.mixer.music.set_volume(
            volume
        )