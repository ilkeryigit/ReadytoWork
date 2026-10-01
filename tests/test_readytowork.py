import pathlib
import unittest.mock as mock

import pytest

import readytowork

ROOT = pathlib.Path(__file__).parent.parent


def test_mutex_adi_markaya_ozgu():
    assert readytowork.MUTEX_NAME == "ReadyToWork.SingleInstance"


def test_tek_ornek_kontrol_bool_donduruyor():
    assert isinstance(readytowork.single_instance(), bool)


def test_main_migrate_ve_ayarlari_yukler():
    with mock.patch("readytowork.single_instance", return_value=True), \
         mock.patch("readytowork.config.migrate_legacy") as migrate, \
         mock.patch("readytowork.config.load", return_value=([], "default", "de")) as loader, \
         mock.patch("readytowork.config.config_path") as config_path, \
         mock.patch("readytowork.app.TrayApp") as tray:
        config_path.return_value.exists.return_value = True
        readytowork.main()
    migrate.assert_called_once_with()
    loader.assert_called_once_with()
    tray.assert_called_once_with([], "default", "de", False)


def test_ilk_calismada_first_run_true():
    with mock.patch("readytowork.single_instance", return_value=True), \
         mock.patch("readytowork.config.migrate_legacy"), \
         mock.patch("readytowork.config.load", return_value=([], "default", "tr")), \
         mock.patch("readytowork.config.config_path") as config_path, \
         mock.patch("readytowork.app.TrayApp") as tray:
        config_path.return_value.exists.return_value = False
        readytowork.main()
    assert tray.call_args[0][3] is True


def test_tek_ornek_kapatirsa_cikis_yapar():
    with mock.patch("readytowork.single_instance", return_value=False), \
         mock.patch("readytowork.config.load") as loader:
        with pytest.raises(SystemExit):
            readytowork.main()
    loader.assert_not_called()


def test_eski_v1_dosyalari_kaldirildi():
    assert not (ROOT / "v1.py").exists()
    assert not (ROOT / "v1.spec").exists()
    assert not (ROOT / "tests" / "test_v1.py").exists()
