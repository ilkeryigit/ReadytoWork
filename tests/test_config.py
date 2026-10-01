import json

import pytest

import config


def test_varsayilan_oge_yok():
    assert not hasattr(config, "DEFAULT_OGELER")
    assert not hasattr(config, "DEFAULT_ITEMS")


def test_config_dizini_appdata_zerinde(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    assert config.config_dir() == tmp_path / "ReadytoWork"


def test_yoksa_bos_liste(tmp_path):
    items, browser, lang = config.load(tmp_path)
    assert items == [] and browser == "default" and lang == "tr"


def test_kaydet_ve_yukle_roundtrip(tmp_path):
    config.save([config.Item("Zotero", "program", "C:/z.exe")], "firefox", "en", tmp_path)
    items, browser, lang = config.load(tmp_path)
    assert items == [config.Item("Zotero", "program", "C:/z.exe")]
    assert browser == "firefox" and lang == "en"


def test_kaydet_uygulama_dizini_olusturur(tmp_path):
    target = tmp_path / "yeni"
    config.save([], "default", "tr", target)
    assert (target / "config.json").exists()


def test_kaydet_tmp_dosya_birakmaz(tmp_path):
    config.save([], "default", "tr", tmp_path)
    assert not (tmp_path / "config.json.tmp").exists()


def test_kaydet_atomik_eski_dosyayi_korur(tmp_path, monkeypatch):
    config.save([config.Item("A", "program", "a.exe")], "default", "tr", tmp_path)
    original = (tmp_path / "config.json").read_text(encoding="utf-8")

    def patla(*_args, **_kwargs):
        raise OSError("disk dolu")

    monkeypatch.setattr(config.os, "replace", patla)
    with pytest.raises(OSError):
        config.save([config.Item("B", "program", "b.exe")], "default", "tr", tmp_path)

    assert (tmp_path / "config.json").read_text(encoding="utf-8") == original
    assert not (tmp_path / "config.json.tmp").exists()


def test_bozuk_json_yedeklenir_ve_bos_doner(tmp_path):
    (tmp_path / "config.json").write_text("{bozuk", encoding="utf-8")
    items, _, _ = config.load(tmp_path)
    assert items == []
    assert (tmp_path / "config.json.bak").exists()


def test_bozuk_json_asli_yerinde_kalir(tmp_path):
    (tmp_path / "config.json").write_text("{bozuk", encoding="utf-8")
    config.load(tmp_path)
    assert (tmp_path / "config.json").read_text(encoding="utf-8") == "{bozuk"


def test_ogeler_duz_olmayan_veri_yoksayilir(tmp_path):
    (tmp_path / "config.json").write_text(
        json.dumps({"items": [
            "metin",
            {"name": "A", "type": "program", "path": "a.exe"},
            {"name": "B", "type": "uydurma", "path": "b"},
            {"name": "", "type": "program", "path": "c"},
        ]}),
        encoding="utf-8")
    items, _, _ = config.load(tmp_path)
    assert [item.name for item in items] == ["A"]


def test_legacy_turkce_alanlar_okunur(tmp_path):
    (tmp_path / "config.json").write_text(
        json.dumps({"tarayici": "varsayilan",
                    "ogeler": [{"ad": "Klasor", "tur": "klasor", "yol": "C:/k"}]}),
        encoding="utf-8")
    items, browser, _ = config.load(tmp_path)
    assert items == [config.Item("Klasor", "folder", "C:/k")]
    assert browser == "default"


def test_gecersiz_browser_dil_default(tmp_path):
    (tmp_path / "config.json").write_text(
        json.dumps({"browser": "opera", "lang": "kl", "items": []}), encoding="utf-8")
    _, browser, lang = config.load(tmp_path)
    assert browser == "default" and lang == "tr"


def test_migrate_legacy_tasar_ve_siler(tmp_path, monkeypatch):
    kaynak = tmp_path / "eski"
    kaynak.mkdir()
    (kaynak / "config.json").write_text(
        json.dumps({"items": [{"name": "A", "type": "url", "path": "https://x"}]}),
        encoding="utf-8")
    hedef = tmp_path / "appdata"
    monkeypatch.setenv("APPDATA", str(hedef))
    monkeypatch.setattr(config, "_legacy_path", lambda: kaynak / "config.json")

    assert config.migrate_legacy() is True
    assert not (kaynak / "config.json").exists()
    items, _, _ = config.load(hedef / "ReadytoWork")
    assert items[0].name == "A"


def test_migrate_legacy_hedef_varken_yapmaz(tmp_path, monkeypatch):
    hedef = tmp_path / "appdata"
    config.save([], "default", "tr", hedef / "ReadytoWork")
    monkeypatch.setenv("APPDATA", str(hedef))
    monkeypatch.setattr(config, "_legacy_path", lambda: tmp_path / "yok.json")
    assert config.migrate_legacy() is False


def test_turkce_karakterler_ayakta():
    assert "Teşekkür" not in "".join(config.VALID_TYPES)
    assert config.VALID_TYPES == ("program", "folder", "document", "url")
