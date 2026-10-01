import os
import subprocess
import webbrowser
from pathlib import Path

from config import Item
from i18n import t

BROWSER_PATHS = {
    "chrome": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ],
    "firefox": [
        r"C:\Program Files\Mozilla Firefox\firefox.exe",
        r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
    ],
    "edge": [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ],
}


def browser_exe(browser: str):
    candidates = list(BROWSER_PATHS.get(browser, []))
    if browser == "chrome":
        local = os.environ.get("LOCALAPPDATA")
        if local:
            candidates.append(str(Path(local) / r"Google\Chrome\Application\chrome.exe"))
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return None


def _missing(item, key, lang):
    return False, t(key, lang).format(name=item.name, path=item.path)


def _launch(item, target, lang):
    try:
        subprocess.Popen(target)
    except OSError as exc:
        return False, t("error.open_failed", lang).format(name=item.name, error=exc)
    return True, ""


def _startfile(item, lang, missing_key="error.not_found"):
    if not os.path.exists(item.path):
        return _missing(item, missing_key, lang)
    try:
        os.startfile(item.path)
    except OSError as exc:
        return False, t("error.open_failed", lang).format(name=item.name, error=exc)
    return True, ""


def _program(item, lang):
    if not os.path.exists(item.path):
        return _missing(item, "error.not_found", lang)
    return _launch(item, [item.path], lang)


def _url(item, browser, lang):
    if browser and browser != "default":
        exe = browser_exe(browser)
        if not exe:
            return False, t("error.browser_not_found", lang).format(
                name=item.name, browser=browser)
        return _launch(item, [exe, item.path], lang)
    try:
        opened = webbrowser.open(item.path)
    except Exception as exc:
        return False, t("error.open_failed", lang).format(name=item.name, error=exc)
    if not opened:
        return _missing(item, "error.url_failed", lang)
    return True, ""


def open_item(item: Item, browser: str = "default", lang: str = None):
    if item.type == "program":
        return _program(item, lang)
    if item.type == "folder":
        return _startfile(item, lang, "error.folder_not_found")
    if item.type == "document":
        return _startfile(item, lang)
    if item.type == "url":
        return _url(item, browser, lang)
    return False, t("error.unknown_type", lang).format(item_type=item.type)
