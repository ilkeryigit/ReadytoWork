<div align="center">

# ReadytoWork

**A Windows tray launcher that puts your programs, folders, documents and URLs one click away.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-0078D4.svg)](https://en.wikipedia.org/wiki/Microsoft_Windows)
[![Python: 3](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Build: PyInstaller](https://img.shields.io/badge/build-PyInstaller-6.x-purple.svg)](https://pyinstaller.org/)
[![Release: 1.0.0](https://img.shields.io/badge/release-1.0.0-brightgreen.svg)](https://github.com/ilkeryigit/ReadytoWork/releases)

[Interface languages](lang/) · English · Türkçe · 中文 · Deutsch · Italiano

</div>

---

## Why

Every morning you open the same handful of things: a document you are writing,
a reference manager, a folder of sources, a dashboard. ReadytoWork keeps them
in one tray menu, so you open all of them with a single click instead of hunting
through the Start menu and your desktop.

It is a small, honest tool: no account, no cloud, no telemetry, no background
network traffic. Your list lives in one JSON file on your own machine.

## Features

- **Tray menu** — every item listed, plus *Open all* for one-click mornings
- **Four item types** — program, folder, document, web address
- **Five languages** — English, Türkçe, 中文, Deutsch, Italiano; switchable at any time
- **Settings that stick** — stored in `%APPDATA%\ReadytoWork\config.json`, written atomically so a crash or a full disk can never corrupt them
- **Reorder and rename** — move items up and down, edit inline
- **Browser choice** — open web addresses in the system default, Chrome, Firefox or Edge
- **Single instance** — launching twice does nothing; it never stacks up
- **Native installer** — Start Menu and desktop shortcuts, optional start-with-Windows, clean uninstaller

## Install

Download the installer from the [releases page](https://github.com/ilkeryigit/ReadytoWork/releases),
run `ReadytoWork-Setup-1.0.0.exe`, and pick your options.

> The installer is not code-signed, so Windows SmartScreen may warn you on first
> run. Choose *More info → Run anyway*.

## Usage

1. Start ReadytoWork. On first launch the settings window opens automatically.
2. Press **Add**, choose a type, give it a name, and pick a path (or paste a URL).
3. Press **Save**. The item is now in your tray menu.
4. Right-click the tray icon → **Open all** to launch everything at once.

Settings are removed when you uninstall the application.

## Building from source

Requires Python 3.10+ on Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# run from source
.\.venv\Scripts\python.exe readytowork.py

# tests
.\.venv\Scripts\python.exe -m pytest tests -v

# single-file executable -> dist\ReadytoWork.exe
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm ReadytoWork.spec

# installer -> dist\ReadytoWork-Setup-1.0.0.exe   (needs Inno Setup 6)
& "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe" installer.iss
```

## Translating

Every user-visible string lives in `lang/<code>.json`. To add a language:

1. Copy `lang/en.json` to `lang/<code>.json`.
2. Translate the values. **Keep the keys identical.**
3. Add the display name to `LANG_NAMES` in `i18n.py`.
4. Run the tests — `tests/test_i18n.py` fails if a key is missing or empty.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## Architecture

```
readytowork.py   entry point, single-instance mutex
app.py           tray icon, dynamic menu, settings thread
gui.py           settings window (tkinter)
config.py        atomic JSON persistence in %APPDATA%
actions.py       opening programs, folders, documents, URLs
i18n.py          translation loading and lookup
lang/*.json      the five catalogs
```

Settings are saved atomically: the new file is written to `config.json.tmp`
and then renamed over `config.json`, so the file on disk is always complete.
A corrupt file is moved to `config.json.bak` and the app starts with an empty
list instead of overwriting anything.

## Privacy

No analytics, no network calls, no user tracking. The only file written outside
the install directory is `%APPDATA%\ReadytoWork\config.json`, which holds the
items you created. The test suite includes an automated check that no personal
paths, usernames or email addresses end up in the repository.

## License

[MIT](LICENSE) © 2026 ilkeryigit
