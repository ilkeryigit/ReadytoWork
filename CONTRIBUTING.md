# Contributing to ReadytoWork

Thanks for helping out. This is a small Windows tool, so contributions are
either bug fixes, translations, or small features that keep it small.

## Getting started

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest tests -v
```

Everything runs on Windows. Open a pull request and describe what changed and why.

## Ground rules

- **Windows only.** The app uses `os.startfile` and a Win32 mutex on purpose.
- **No new runtime dependencies.** Standard library, `pystray` and `Pillow` only.
- **Code identifiers are English.** User-visible strings are translated, never
  hardcoded in the source.
- **Every string goes through `t()`.** If you add a label, add its key to all
  five catalogs in the same commit — the tests will tell you if you forget.
- **No personal data.** Do not commit real paths, usernames or email addresses.
  `tests/test_privacy.py` enforces this.

## Tests

Tests must run on Windows and must never perform real system actions:
`subprocess.Popen`, `os.startfile` and `webbrowser.open` are always mocked.

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

## Adding a translation

This is the easiest contribution.

1. Copy `lang/en.json` to `lang/<code>.json`.
2. Translate the **values**. Leave the **keys** exactly as they are.
3. Add the language name to `LANG_NAMES` in `i18n.py`:

   ```python
   LANG_NAMES = {..., "fr": "Français"}
   ```

4. Run the tests. `tests/test_i18n.py` checks that every catalog has the same
   key set, that no value is empty, and that no encoding damage crept in.

Placeholders such as `{name}` and `{path}` must survive translation — they are
filled in at runtime.

## Reporting bugs

Open an issue with your Windows version, what you expected, and what happened
instead. If something fails on startup, the tray notification or
`%APPDATA%\ReadytoWork\config.json` (with personal paths removed) helps a lot.

By contributing you agree that your work is licensed under the MIT License.
