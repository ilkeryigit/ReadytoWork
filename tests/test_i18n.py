import pytest

import i18n

LANGS = ("tr", "en", "zh", "de", "it")


def test_versiyon_bir_nokta_sifir_sifir():
    from version import __version__
    assert __version__ == "1.0.0"


def test_bes_dil_dosyasi_yukleniyor():
    assert set(i18n.load_languages()) == set(LANGS)


def test_bos_anahtar_geri_donuyor():
    assert i18n.t("yok.boyle.bir.anahtar") == "yok.boyle.bir.anahtar"


def test_gecersiz_dil_anahtar_donduruyor():
    assert i18n.t("tray.quit", "xx") == i18n.t("tray.quit", "tr")


@pytest.mark.parametrize("code", LANGS)
def test_tr_anahtarlari_diger_dillerde_var(code):
    tr = set(i18n.load_languages()["tr"])
    assert tr <= set(i18n.load_languages()[code])


def test_anahtar_setleri_ayni():
    reference = set(i18n.load_languages()["tr"])
    for code in LANGS:
        assert set(i18n.load_languages()[code]) == reference


@pytest.mark.parametrize("code", LANGS)
def test_bos_metin_yok(code):
    for key, value in i18n.load_languages()[code].items():
        assert value.strip(), f"{code}:{key}"


@pytest.mark.parametrize("code", LANGS)
def test_yerine_koyma_isareti_kalinti_yok(code):
    joined = "".join(i18n.load_languages()[code].values())
    assert "\ufffd" not in joined, code


def test_dil_adi_kendi_dilinde():
    assert i18n.LANG_NAMES["tr"] == "Türkçe"
    assert i18n.LANG_NAMES["en"] == "English"
