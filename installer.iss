; Simple Timer - Inno Setup script
; 新しいバージョンを出すときは、下の MyAppVersion を version.py の VERSION と同じ番号に書き換えてください。
; AppId は v1.1.0 から引き継いでいます。変更しないでください（変更すると上書きアップデートではなく別アプリとして扱われます）。

#define MyAppName "Simple Timer"
#define MyAppVersion "1.2.0"
#define MyAppPublisher "Matsuri-code"
#define MyAppExeName "SimpleTimer.exe"

[Setup]
AppId={{AEECAC16-2B78-414D-A59E-405EEEF7291B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer
OutputBaseFilename=SimpleTimer_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "デスクトップにアイコンを作成 / Create a desktop icon"; GroupDescription: "追加タスク / Additional tasks:"

[Files]
Source: "dist\SimpleTimer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Simple Timer を起動 / Launch Simple Timer"; Flags: nowait postinstall skipifsilent
