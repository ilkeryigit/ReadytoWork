import json
import os
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import i18n

APP_NAME = "ReadytoWork"
VALID_TYPES = ("program", "folder", "document", "url")
VALID_BROWSERS = ("default", "chrome", "firefox", "edge")
DEFAULT_BROWSER = "default"
DEFAULT_LANG = "tr"
LEGACY_VALUES = {"klasor": "folder", "belge": "document", "varsayilan": "default"}


@dataclass
class Item:
    name: str
    type: str
    path: str


def config_dir() -> Path:
    return Path(os.environ["APPDATA"]) / APP_NAME


def config_path() -> Path:
    return config_dir() / "config.json"


def _legacy_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent / "config.json"
    return Path(__file__).parent / "config.json"


def _backup(path: Path) -> None:
    try:
        shutil.copy2(path, path.with_suffix(".json.bak"))
    except OSError:
        pass


def _normalize(value):
    return LEGACY_VALUES.get(value, value)


def _items_from(data) -> list:
    if not isinstance(data, dict):
        return None
    raw = data.get("items") or data.get("ogeler")
    if not isinstance(raw, list):
        return None
    items = []
    for record in raw:
        if not isinstance(record, dict):
            continue
        name = record.get("name") or record.get("ad")
        item_type = _normalize(record.get("type") or record.get("tur"))
        path = record.get("path") or record.get("yol")
        if name and path and item_type in VALID_TYPES:
            items.append(Item(str(name), str(item_type), str(path)))
    return items


def _pick(data, key: str, legacy_key: str, allowed, default: str) -> str:
    if not isinstance(data, dict):
        return default
    value = _normalize(data.get(key) or data.get(legacy_key))
    return str(value) if value in allowed else default


def load(directory=None) -> tuple:
    path = (Path(directory) if directory else config_dir()) / "config.json"
    if not path.exists():
        return [], DEFAULT_BROWSER, DEFAULT_LANG
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        _backup(path)
        return [], DEFAULT_BROWSER, DEFAULT_LANG
    items = _items_from(data)
    if items is None:
        _backup(path)
        return [], DEFAULT_BROWSER, DEFAULT_LANG
    return (items,
            _pick(data, "browser", "tarayici", VALID_BROWSERS, DEFAULT_BROWSER),
            _pick(data, "lang", "dil", tuple(i18n.load_languages()), DEFAULT_LANG))


def save(items, browser: str, lang: str, directory=None) -> None:
    folder = Path(directory) if directory else config_dir()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "config.json"
    tmp = folder / "config.json.tmp"
    payload = json.dumps({"browser": browser, "lang": lang,
                          "items": [asdict(item) for item in items]},
                         ensure_ascii=False, indent=2)
    try:
        tmp.write_text(payload, encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        try:
            tmp.unlink()
        except OSError:
            pass
        raise


def migrate_legacy() -> bool:
    if config_path().exists():
        return False
    legacy = _legacy_path()
    if not legacy.exists():
        return False
    items, browser, lang = load(legacy.parent)
    save(items, browser, lang)
    legacy.unlink()
    return True
