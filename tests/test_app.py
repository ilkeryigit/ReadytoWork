import unittest.mock as mock

import app
import config


def test_app_adi():
    assert app.APP_NAME == "ReadytoWork"


def test_kaydet_basarili_menu_yeniler():
    uygulama = app.TrayApp([], "default", "tr")
    with mock.patch.object(uygulama, "build_menu") as builder, \
         mock.patch("app.config.save") as saver:
        assert uygulama.save_and_refresh([], "firefox", "en") is True
    saver.assert_called_once()
    builder.assert_called()


def test_kaydet_hatasinda_menu_yenilenmez():
    uygulama = app.TrayApp([], "default", "tr")
    with mock.patch("app.config.save", side_effect=OSError("disk dolu")), \
         mock.patch.object(uygulama, "build_menu") as builder:
        assert uygulama.save_and_refresh([], "default", "tr") is False
    builder.assert_not_called()


def test_kaydet_hatasinda_bildirim_gider():
    uygulama = app.TrayApp([], "default", "tr")
    uygulama.icon = mock.Mock()
    with mock.patch("app.config.save", side_effect=OSError("disk dolu")):
        assert uygulama.save_and_refresh([], "default", "tr") is False
    uygulama.icon.notify.assert_called_once()
    assert "Kaydedilemedi" in uygulama.icon.notify.call_args[0][0]


def test_dil_degisince_menu_guncellenir():
    uygulama = app.TrayApp([], "default", "tr")
    with mock.patch("app.config.save"):
        uygulama.save_and_refresh([], "default", "de")
    assert uygulama.lang == "de"


def test_menu_ogeleri_kullanim_tercihi():
    uygulama = app.TrayApp([config.Item("A", "url", "https://x")], "default", "tr")
    assert uygulama.build_menu() is not None


def test_menu_bos_listeyle_de_olusur():
    assert app.TrayApp([], "default", "tr").build_menu() is not None


def test_bulunamayan_oge_etiketi_ceviri_ile():
    with mock.patch("app.os.path.exists", return_value=False):
        uygulama = app.TrayApp([config.Item("A", "program", "C:/yok.exe")], "default", "en")
        assert uygulama.build_menu() is not None


def test_oge_tiklama_hatayi_bildirir():
    uygulama = app.TrayApp([], "default", "tr")
    ikon = mock.Mock()
    item = config.Item("A", "program", "C:/yok.exe")
    with mock.patch("app.actions.open_item", return_value=(False, "hata")):
        uygulama._on_item(ikon, item)
    ikon.notify.assert_called_once_with("hata", "ReadytoWork")


def test_hepsini_ac_ilk_uc_hatayi_bildirir():
    uygulama = app.TrayApp([], "default", "tr")
    uygulama.items = [config.Item(str(n), "program", "x") for n in range(5)]
    ikon = mock.Mock()
    with mock.patch("app.actions.open_item", return_value=(False, "hata")):
        uygulama._open_all(ikon, None)
    bildirilen = ikon.notify.call_args[0][0]
    assert bildirilen.count("hata") == 3


def test_ayarlar_penceresi_iki_kez_acilmaz():
    uygulama = app.TrayApp([], "default", "tr")
    uygulama._settings_open = True
    with mock.patch("app.threading.Thread") as thread:
        uygulama._open_settings(mock.Mock(), None)
    thread.assert_not_called()


def test_ilk_calismada_ayarlar_acilir():
    uygulama = app.TrayApp([], "default", "tr", first_run=True)
    with mock.patch("app.threading.Timer") as timer, \
         mock.patch.object(uygulama.icon, "run"):
        uygulama.run()
    timer.assert_called_once()


def test_normal_calismada_ayarlar_acilmaz():
    uygulama = app.TrayApp([], "default", "tr", first_run=False)
    with mock.patch("app.threading.Timer") as timer, \
         mock.patch.object(uygulama.icon, "run") as run:
        uygulama.run()
    timer.assert_not_called()
    run.assert_called_once()


def test_ikon_gri_yedek_donduruyor():
    with mock.patch("app.Path.exists", return_value=False):
        assert app.icon_image().size == (64, 64)
