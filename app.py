import os
import sys
import threading
from pathlib import Path

import pystray
from PIL import Image

import actions
import config
import gui
import i18n

APP_NAME = "ReadytoWork"


def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent


def icon_image() -> Image.Image:
    path = _base_dir() / "app.ico"
    if path.exists():
        return Image.open(path)
    return Image.new("RGB", (64, 64), (26, 115, 232))


class TrayApp:
    def __init__(self, items, browser, lang, first_run: bool = False):
        self.items = list(items)
        self.browser = browser
        self.lang = i18n.set_lang(lang)
        self.first_run = first_run
        self._settings_open = False
        self.icon = pystray.Icon(APP_NAME, icon_image(), APP_NAME, self.build_menu())

    def run(self):
        if self.first_run:
            threading.Timer(1.5, lambda: self._open_settings(self.icon, None)).start()
        self.icon.run()

    def build_menu(self):
        entries = []
        for item in self.items:
            if item.type == "url" or os.path.exists(item.path):
                label = item.name
            else:
                label = i18n.t("tray.missing", self.lang).format(name=item.name)
            entries.append(pystray.MenuItem(label, self._item_callback(item)))
        if entries:
            entries.append(pystray.Menu.SEPARATOR)
        entries.append(pystray.MenuItem(
            i18n.t("tray.open_all", self.lang), self._open_all, default=True))
        entries.append(pystray.Menu.SEPARATOR)
        entries.append(pystray.MenuItem(
            i18n.t("tray.settings", self.lang), self._open_settings))
        entries.append(pystray.MenuItem(
            i18n.t("tray.quit", self.lang), self._quit))
        return pystray.Menu(*entries)

    def _item_callback(self, item):
        return lambda icon, _selected: self._on_item(icon, item)

    def _on_item(self, icon, item):
        ok, message = actions.open_item(item, self.browser, self.lang)
        if not ok:
            icon.notify(message, APP_NAME)

    def _open_all(self, icon, _selected):
        errors = []
        for item in self.items:
            ok, message = actions.open_item(item, self.browser, self.lang)
            if not ok:
                errors.append(message)
        if errors:
            icon.notify("\n".join(errors[:3]), APP_NAME)

    def _open_settings(self, icon, _selected):
        if self._settings_open:
            return
        self._settings_open = True

        def _run():
            try:
                gui.settings_window(
                    list(self.items), self.browser, self.lang,
                    lambda items, browser, lang: self.save_and_refresh(items, browser, lang))
            finally:
                self._settings_open = False

        threading.Thread(target=_run, daemon=True).start()

    def save_and_refresh(self, items, browser, lang) -> bool:
        try:
            config.save(items, browser, lang)
        except OSError as exc:
            self.icon.notify(
                i18n.t("error.save_failed", self.lang).format(error=exc), APP_NAME)
            return False
        self.items = list(items)
        self.browser = browser
        self.lang = i18n.set_lang(lang)
        self.icon.menu = self.build_menu()
        return True

    def _quit(self, icon, _selected):
        icon.stop()
        os._exit(0)
