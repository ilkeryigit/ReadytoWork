import tkinter as tk
import unittest.mock as mock

import config
import gui
import i18n
import pytest


@pytest.fixture
def tk_root():
    """A real Tk root. The dialog wires real widgets, so it can only be checked
    by building it. Skipped where tcl/tk cannot be read (see CONTRIBUTING)."""
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        pytest.skip(f"Tk cannot start in this environment: {exc}")
    root.update()
    yield root
    root.destroy()


def _widgets(widget, kind):
    found = []
    for child in widget.winfo_children():
        if isinstance(child, kind):
            found.append(child)
        found.extend(_widgets(child, kind))
    return found


def test_ekle_penceresi_kaydedebiliyor(tk_root):
    """Regression: the dialog raised UnboundLocalError while being built, so its
    Save button was never created and no item could be added at all."""
    gui.refresh_labels("tr")
    items = []
    gui._edit_dialog(tk_root, None, items, lambda: None, lambda: None)
    tk_root.update()
    dialog = tk_root.winfo_children()[-1]
    entries = [w for w in _widgets(dialog, tk.Entry) if type(w) is tk.Entry]
    entries[0].insert(0, "Zotero")
    entries[1].insert(0, "C:/z.exe")
    kaydet = next(b for b in _widgets(dialog, tk.Button)
                  if b.cget("text") == i18n.t("dialog.ok", "tr"))
    kaydet.invoke()
    assert items == [config.Item("Zotero", "program", "C:/z.exe")]


def test_bes_dil_kodu():
    assert len(gui.LANG_CODES) == 6
    assert "tr" in gui.LANG_CODES and "en" in gui.LANG_CODES


def test_tur_etiketleri_tum_turleri_kapsar():
    gui.refresh_labels("tr")
    assert set(gui.TYPE_LABELS) == {"program", "folder", "document", "url"}


def test_browser_etiketleri_tum_browserlari_kapsar():
    gui.refresh_labels("tr")
    assert set(gui.BROWSER_LABELS) == {"default", "chrome", "firefox", "edge"}


def test_etiketler_dil_degisince_yenilenir():
    gui.refresh_labels("tr")
    turkce = gui.TYPE_LABELS["folder"]
    gui.refresh_labels("en")
    assert gui.TYPE_LABELS["folder"] != turkce
    assert gui.TYPE_LABELS["folder"] == "Folder"
    gui.refresh_labels("tr")
    assert gui.TYPE_LABELS["folder"] == turkce


def test_basarili_kaydet_pencereyi_kapatir():
    state = {"dirty": True}
    destroy = mock.Mock()
    ok = gui.commit([], "default", "tr", lambda i, b, l: True, destroy, state)
    assert ok is True
    destroy.assert_called_once()
    assert state["dirty"] is False


def test_basarisiz_kaydet_pencereyi_kapatmaz():
    state = {"dirty": True}
    destroy = mock.Mock()
    ok = gui.commit([], "default", "tr", lambda i, b, l: False, destroy, state)
    assert ok is False
    destroy.assert_not_called()
    assert state["dirty"] is True


def test_kaydet_argumanlari_dogru_gecer():
    state = {"dirty": True}
    seen = {}

    def on_save(items, browser, lang):
        seen["args"] = (items, browser, lang)
        return True

    gui.commit([], "firefox", "de", on_save, mock.Mock(), state)
    assert seen["args"] == ([], "firefox", "de")


def test_settings_window_imza_dogru():
    import inspect
    parameters = list(inspect.signature(gui.settings_window).parameters)
    assert parameters == ["items", "browser", "lang", "on_save"]
