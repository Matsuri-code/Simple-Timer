# Simple Timer

[日本語](#日本語) | [English](#english)

<p align="center">
  <img src="docs/screenshot_ja.png" alt="Simple Timer (日本語)" width="260">
  <img src="docs/screenshot_en.png" alt="Simple Timer (English)" width="260">
</p>

---

<a id="日本語"></a>

## 日本語

### 概要

Simple Timer は、Python（Tkinter）で作られたシンプルなデスクトップ用タイマー／ストップウォッチアプリです。
最大3つのタイマーを、それぞれ別ウィンドウで同時に動かせます。

### 主な機能

- **タイマー**：秒数を入力してカウントダウン
- **ストップウォッチ**：0 から経過時間を計測
- **一時停止 / 再開 / 停止 / リセット**
- **複数ウィンドウ**：最大3つまで同時に起動可能
- **アラーム設定**
  - アラーム音のファイルを好きなものに変更可能
  - アラームの再生時間を 5〜30 秒の範囲で設定可能
- **Windows 通知**：タイマー終了時にトースト通知を表示（Windows のみ）
- **テーマ変更**：ボタンでテーマを順番に切り替え（開いている全ウィンドウに反映）
- **日本語 / English 切り替え**：ボタンで即時に切り替え（開いている全ウィンドウに反映）
- **アップデート確認**：起動時に新しいバージョンがあれば通知し、リリースページを開けます

### 動作環境

- Python 3.x（Tkinter が使える環境）
- OS：Windows / macOS / Linux
  - ※ Windows 以外ではトースト通知は表示されず、代わりにコンソールへメッセージが出力されます

### インストール

```bash
git clone https://github.com/Matsuri-code/Simple-Timer.git
cd Simple-Timer
```

次のコマンドで、必要なパッケージをまとめてインストールします。

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` に含まれるパッケージ：

| パッケージ | 用途 |
| --- | --- |
| `pygame` | アラーム音（mp3 / wav）の再生 |
| `requests` | アップデート確認（GitHub Releases の取得） |
| `windows-toasts` | Windows のトースト通知（Windows のみ） |

### 起動方法

```bash
python main.py
```

※ エントリーポイントのファイル名は、実際のファイル名に読み替えてください。

### 使い方

1. 入力欄に**秒数**（整数）を入力します。例：`180`（3分）
2. 「**タイマー開始**」ボタン、または **Enter キー**でカウントダウンを開始します。
3. 「**ストップウォッチ**」を押すと、0 から経過時間を計測します。
4. 「**一時停止**」「**再開**」「**停止**」「**リセット**」で操作できます。
5. 「**新しいタイマー**」で別ウィンドウのタイマーを追加できます（最大3つ）。
6. 終了時にアラーム音が鳴り、通知とダイアログが表示されます。

### ボタン一覧

| ボタン | 説明 |
| --- | --- |
| タイマー開始 | 入力した秒数でカウントダウンを開始 |
| ストップウォッチ | 0 から経過時間の計測を開始 |
| 一時停止 | 動作中のタイマー / ストップウォッチを一時停止 |
| 再開 | 一時停止を解除して再開 |
| 停止 | タイマー / ストップウォッチを停止 |
| リセット | 停止して表示を `00:00` に戻す |
| テーマ変更 | 配色テーマを次のものに切り替え |
| アラーム音選択 | アラーム音のファイルを選択 |
| アラーム時間設定 | アラームの再生時間（5〜30秒）を設定 |
| 新しいタイマー | 別ウィンドウのタイマーを追加（最大3つ） |
| English | 表示言語を英語に切り替え |

### 注意事項

- タイマーの入力単位は**秒**です（1以上の整数）。
- テーマ・言語・アラーム設定などは、**すべてのウィンドウを閉じたとき**に保存されます。
- メインウィンドウを閉じると、他のタイマーウィンドウも一緒に閉じます。
- アラーム音は **mp3 / wav** ファイルを選択できます。アラーム音を選んでいない状態でタイマーが終了すると、警告が表示されます。
- 音声デバイスが使えない環境でもアプリは起動しますが、アラーム音は鳴りません。
- ネットワークに接続できない場合、アップデート確認は自動的にスキップされます。

### ファイル構成

| ファイル | 説明 |
| --- | --- |
| `main.py` | アプリ本体（タイマーウィンドウ・ウィンドウ管理） |
| `updater.py` | アップデート確認 |
| `settings.py` | 設定の読み込み・保存 |
| `themes.py` | テーマ定義 |
| `audio.py` | アラーム音の再生・選択 |
| `translations.py` | 日本語 / 英語の翻訳テキスト |
| `version.py` | アプリ名・バージョン・ウィンドウサイズ |

### ライセンス

All rights reserved.
本ソフトウェアの著作権は作者（Matsuri-code）に帰属します。ソースコード・実行ファイル（インストーラー / exe）を問わず、無断での複製・改変・再配布・再利用を禁止します。

### プライバシーポリシー

本アプリは個人情報を収集しません。詳細は [PRIVACY.md](PRIVACY.md) をご覧ください。

---

<a id="english"></a>

## English

### Overview

Simple Timer is a simple desktop timer / stopwatch app built with Python (Tkinter).
You can run up to three timers at the same time, each in its own window.

### Features

- **Timer**: enter a number of seconds and count down
- **Stopwatch**: measure elapsed time from 0
- **Pause / Resume / Stop / Reset**
- **Multiple windows**: up to 3 at once
- **Alarm settings**
  - Choose your own alarm sound file
  - Set the alarm duration between 5 and 30 seconds
- **Windows notifications**: shows a toast notification when the timer finishes (Windows only)
- **Theme switching**: cycle through color themes with a button (applied to all open windows)
- **Japanese / English toggle**: switch the UI language instantly (applied to all open windows)
- **Update check**: on startup, notifies you if a new version is available and can open the release page

### Requirements

- Python 3.x (with Tkinter available)
- OS: Windows / macOS / Linux
  - Note: on non-Windows platforms, toast notifications are not shown; a message is printed to the console instead

### Installation

```bash
git clone https://github.com/Matsuri-code/Simple-Timer.git
cd Simple-Timer
```

Install all required packages with the following command:

```bash
python -m pip install -r requirements.txt
```

Packages included in `requirements.txt`:

| Package | Purpose |
| --- | --- |
| `pygame` | Alarm sound playback (mp3 / wav) |
| `requests` | Update check (fetching GitHub Releases) |
| `windows-toasts` | Windows toast notifications (Windows only) |

### Running

```bash
python main.py
```

Replace `main.py` with the actual name of your entry-point file.

### Usage

1. Enter a number of **seconds** (integer) in the input field. Example: `180` (3 minutes)
2. Click **Start Timer** or press the **Enter key** to begin the countdown.
3. Click **Stopwatch** to measure elapsed time from 0.
4. Use **Pause**, **Resume**, **Stop**, and **Reset** to control it.
5. Click **New Timer** to open another timer window (up to 3).
6. When the timer finishes, the alarm sounds and a notification and dialog are shown.

### Buttons

| Button | Description |
| --- | --- |
| Start Timer | Start counting down from the entered number of seconds |
| Stopwatch | Start measuring elapsed time from 0 |
| Pause | Pause the running timer / stopwatch |
| Resume | Resume after pausing |
| Stop | Stop the timer / stopwatch |
| Reset | Stop and return the display to `00:00` |
| Change Theme | Switch to the next color theme |
| Select Alarm Sound | Choose the alarm sound file |
| Set Alarm Duration | Set how long the alarm plays (5–30 seconds) |
| New Timer | Open an additional timer window (up to 3) |
| 日本語 | Switch the UI language to Japanese |

### Notes

- The timer input unit is **seconds** (an integer of 1 or more).
- Theme, language, and alarm settings are saved **when all windows are closed**.
- Closing the main window also closes all other timer windows.
- You can choose **mp3 / wav** files as the alarm sound. If no alarm sound is selected when the timer finishes, a warning is shown.
- The app still starts on machines without a usable audio device, but the alarm will not play.
- If the network is unavailable, the update check is skipped automatically.

### Project Structure

| File | Description |
| --- | --- |
| `main.py` | Main app (timer windows and window management) |
| `updater.py` | Update checking |
| `settings.py` | Loading and saving settings |
| `themes.py` | Theme definitions |
| `audio.py` | Alarm sound playback and selection |
| `translations.py` | Japanese / English translation strings |
| `version.py` | App name, version, and window size |

### License

All rights reserved.
This software is copyrighted by the author (Matsuri-code). Copying, modifying, redistributing, or reusing this software — whether the source code or the compiled application (installer / exe) — without permission is prohibited.

### Privacy Policy

This app does not collect any personal information. See [PRIVACY.md](PRIVACY.md) for details.
