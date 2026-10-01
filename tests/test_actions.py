import unittest.mock as mock
from pathlib import Path

import actions
import config

ROOT = Path(__file__).parent.parent
SOURCE_FILES = [p for p in ROOT.glob("*.py")]


def _item(**overrides) -> config.Item:
    base = {"name": "A", "type": "program", "path": "C:/a.exe"}
    base.update(overrides)
    return config.Item(**base)


def test_api_ingilizce_adlarla():
    assert hasattr(actions, "open_item")
    assert not hasattr(actions, "ac")


def test_program_popen_cagirir():
    with mock.patch("actions.os.path.exists", return_value=True), \
         mock.patch("actions.subprocess.Popen") as popen:
        assert actions.open_item(_item()) == (True, "")
    popen.assert_called_once_with(["C:/a.exe"])


def test_program_yoksa_hata_mesaji():
    with mock.patch("actions.os.path.exists", return_value=False):
        ok, message = actions.open_item(_item(), lang="en")
    assert ok is False and "not found" in message


def test_klasor_startfile():
    with mock.patch("actions.os.path.exists", return_value=True), \
         mock.patch("actions.os.startfile") as startfile:
        assert actions.open_item(_item(type="folder"), lang="tr") == (True, "")
    startfile.assert_called_once_with("C:/a.exe")


def test_klasor_yoksa_klasor_mesaji():
    with mock.patch("actions.os.path.exists", return_value=False):
        ok, message = actions.open_item(_item(type="folder"), lang="en")
    assert ok is False and "folder not found" in message


def test_belge_startfile():
    with mock.patch("actions.os.path.exists", return_value=True), \
         mock.patch("actions.os.startfile"):
        assert actions.open_item(_item(type="document"), lang="en") == (True, "")


def test_url_varsayilan_webbrowser():
    with mock.patch("actions.webbrowser.open", return_value=True) as opener:
        assert actions.open_item(_item(type="url", path="https://x"), "default") == (True, "")
    opener.assert_called_once_with("https://x")


def test_url_secili_browser():
    with mock.patch("actions.browser_exe", return_value="chrome.exe"), \
         mock.patch("actions.subprocess.Popen") as popen:
        ok, _ = actions.open_item(_item(type="url", path="https://x"), "chrome")
    assert ok is True
    popen.assert_called_once_with(["chrome.exe", "https://x"])


def test_url_browser_bulunamadi():
    with mock.patch("actions.browser_exe", return_value=None):
        ok, message = actions.open_item(_item(type="url", path="https://x"), "opera", lang="en")
    assert ok is False and "browser" in message.lower()


def test_bilinmeyen_tur():
    ok, message = actions.open_item(_item(type="uydurma"), lang="tr")
    assert ok is False and "Bilinmeyen" in message


def test_mesajlar_dile_gore_degisir():
    with mock.patch("actions.os.path.exists", return_value=False):
        _, turkce = actions.open_item(_item(), lang="tr")
        _, almanca = actions.open_item(_item(), lang="de")
        _, cince = actions.open_item(_item(), lang="zh")
    assert len({turkce, almanca, cince}) == 3


def test_acma_hatasi_yakalanir():
    with mock.patch("actions.os.path.exists", return_value=True), \
         mock.patch("actions.subprocess.Popen", side_effect=OSError("yok")):
        ok, message = actions.open_item(_item(), lang="en")
    assert ok is False and "Could not open" in message


def test_browser_exe_bulunamaz():
    with mock.patch("actions.os.path.exists", return_value=False):
        assert actions.browser_exe("chrome") is None


def test_kaynaklarda_yerine_koyma_isareti_yok():
    for path in SOURCE_FILES:
        assert "\ufffd" not in path.read_text(encoding="utf-8"), path.name
