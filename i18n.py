import json
from pathlib import Path

LANG_DIR = Path(__file__).parent / "lang"
DEFAULT_LANG = "tr"
LANG_NAMES = {"tr": "Türkçe", "en": "English", "zh": "中文", "de": "Deutsch", "it": "Italiano", "fr": "Français"}

_catalog: dict = {}
_active = DEFAULT_LANG


def load_languages() -> dict:
    global _catalog
    if not _catalog:
        for path in sorted(LANG_DIR.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(data, dict):
                _catalog[path.stem] = {str(k): str(v) for k, v in data.items()}
    return _catalog


def set_lang(code: str) -> str:
    global _active
    _active = code if code in load_languages() else DEFAULT_LANG
    return _active


def get_lang() -> str:
    return _active


def t(key: str, lang: str = None) -> str:
    catalog = load_languages()
    return (catalog.get(lang or _active) or {}).get(key) \
        or (catalog.get(DEFAULT_LANG) or {}).get(key) \
        or key
