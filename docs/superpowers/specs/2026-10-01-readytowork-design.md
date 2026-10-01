# ReadytoWork — Tasarım Spesifikasyonu

**Tarih:** 2026-10-01
**Durum:** Onaylandı
**Sürüm:** 1.0.0

---

## 1. Problem

Uygulamada ayarlar kaydediliyor ama bir süre sonra en eski ayarlara dönüyor.
Ayrıca uygulama kişisel belge yollarıyla hardcoded, tek dillidir,
kurulum paketi yoktur ve dünya çapında paylaşıma uygun değildir.

### 1.1 Kayıt hatasının kök nedeni

Üç katmanlıdır ve birbirini besler:

1. **`config.py:30` — config EXE'nin yanına yazılıyor.**
   `_temel_dizin()` → `Path(sys.executable).parent`.
   Geliştirme kopyası ile kurulmuş kopyası **iki ayrı config dosyası**
   demektir. Biri kaydediyor, diğeri eskisini gösteriyor.

2. **`gui.py:140` — sessiz veri kaybı.**
   `kaydet()` içinde `on_kaydet(...)` OSError fırlatırsa bile `root.destroy()`
   çalışıyor. Kullanıcı "Kaydedilemedi" bildirimini kaçırırsa kaydedildi
   sanıyor.

3. **`config.py:87` — atomik olmayan yazım.**
   `Path.write_text()` yarım kalmış dosya bırakabilir; eski içerik ya da
   bozuk JSON kalır. Bir sonraki açılışta `load()` parse hatası yakalayıp
   varsayılana düşüyor → "en eski ayarlar".

Doğrulama: çalışan kurulumda `config.json` **hiçbir yerde yok**
(masaüstü, dist, repo kökü, %APPDATA% taranmış). Kayıp veri yoktur.
Kaydetme zinciri (GUI butonu → `on_kaydet` → `config.kaydet`) kod düzeyinde
sağlam çalışıyor; kırılma noktası dosya konumu ve yazım garantisi.

---

## 2. Mimari

### 2.1 Modüller

| Modül | Sorumluluk |
|---|---|
| `config.py` | `Item` dataclass, `%APPDATA%` yolu, atomik `save`/`load` |
| `i18n.py` | `lang/*.json` yükleme, `t()` çeviri, aktif dil |
| `actions.py` | `open_item(item, browser)` — program/klasör/belge/url açma |
| `app.py` | `TrayApp` — pystray ikonu, dinamik menü, tek örnek |
| `gui.py` | tkinter ayarlar penceresi (i18n'li) |
| `readytowork.py` | Giriş noktası: modülleri başlatır, tek örnek mutex'i (`v1.py`'den yeniden adlandırılır) |
| `version.py` | `__version__ = "1.0.0"` — tek doğruluk kaynağı |
| `lang/*.json` | `tr, en, zh, de, it` çeviri dosyaları |

Modül adları zaten İngilizce. Tek örnek mutex adı dil-bağımsız ve markaya
özgüdür: `ReadyToWork.SingleInstance` — eski Türkçe ad kullanılmaz, böylece
kurulu sürüm ile taşınabilir eski kopya birbirini mutex'e kilitlemez.

### 2.2 Veri akışı

```
app.py: ikon.run()  (tek örnek mutex → çıkış)
  └─ Ayarlar... → thread → gui.settings_window(items, on_save)
       └─ Kaydet → on_save(items, browser, lang)
            └─ app._save_and_refresh() → config.save()
                                          ├─ .tmp yaz → os.replace()  (atomik)
                                          ├─ başarı: menü yenile, pencere kapanır
                                          └─ OSError: pencere AÇIK kalır, hata gösterilir
```

### 2.3 Tanımlayıcı adları

GitHub katkıcı dostu olması için tüm fonksiyon/değişken adları
**İngilizceye** çevrilir (`load`/`save`, `item.type`, `settings_window`).
Modül adları zaten İngilizce.

**Sadece kullanıcı girdisi olan şeyler Türkçe kalabilir:** UI metinleri
`lang/*.json` içinde.

---

## 3. Ayar sistemi

### 3.1 Konum

```
%APPDATA%\ReadytoWork\
    config.json
    config.json.bak
```

`Path(os.environ["APPDATA"]) / "ReadytoWork"`.
EXE nereye kurulursa kurulsun, taşınsa, silinse bile ayarlar kalıcıdır.

### 3.2 Atomik yazım

```python
tmp = path.with_suffix(".json.tmp")
tmp.write_text(json, encoding="utf-8")
os.replace(tmp, path)          # atomik: ya tam eski ya tam yeni
```

Yazma başarısızsa `tmp` silinir, **eski dosya korunur**, `OSError` fırlatılır.

### 3.3 Yükleme

- Dosya yoksa → boş liste + varsayılan tarayıcı + sistem dili
- Bozuk JSON → `.bak` kopyası alınır, boş listeye düşülür (sessizce)
- Geçersiz `tur`/`dil`/`tarayici` alanları atlanır, geçerli olanlar alınır

### 3.4 Geriye uyum

EXE'nin yanında eski `config.json` varsa bir kez okunup `%APPDATA%`'ya
taşınır, sonra **silinir**. Dosyanın yokluğu "zaten taşındı" anlamına gelir;
ayrı bir `legacy_migrated` bayrağına gerek yok.

### 3.5 Tarayıcı seçimi

`BROWSERS`: sabit 4 seçenek, her zaman listelenir —
Chrome, Firefox, Edge, **Varsayılan (sistem)**.
`Varsayılan` → `webbrowser.open`; diğerleri → `BROWSERS` sözlüğündeki exe yolu.
Algılama/kurulum mantığı yok, liste sabittir (basitlik).

### 3.6 Kayıt garantileri

| Durum | Sonuç |
|---|---|
| Program kapatılır | ayarlar kalır |
| Bilgisayar yeniden başlar | ayarlar kalır |
| EXE taşınır/silinir | ayarlar kalır |
| Pencere X ile kapatılır | uyarı: "Kaydedilmemiş değişiklik var" |
| Kaydetme başarısız | **pencere açık kalır**, hata gösterilir |
| **Program kaldırılır** | **her şey silinir** (normal uninstall davranışı) |

---

## 4. Çok dillilik

### 4.1 Yapı

```
lang/
    tr.json   en.json   zh.json   de.json   it.json
i18n.py
```

- `t(key, lang=None)` → çeviri; **bulunamazsa `key` döner** (boş ekran yok)
- `load_languages()` → klasördeki tüm `.json` dosyalarını tarar
- Dil listesi **dosyalardan** üretilir → yeni dil = 1 dosya + 0 kod
- Aktif dil `config.json`'da `"lang": "tr"` olarak saklanır

### 4.2 Anahtar isimlendirme

Nokta ile gruplanmış: `settings.window.title`, `tray.settings`,
`type.program`, `error.not_found`.

### 4.3 Kapsam (~55 metin)

| Grup | Örnekler |
|---|---|
| Tray menü | Ayarlar…, Çıkış, Hepsini Aç, (bulunamadı) |
| Ayar penceresi | Ekle, Düzenle, Sil, Yukarı, Aşağı, Kaydet, Vazgeç, Dil, Tarayıcı |
| Tarayıcı etiketleri | Chrome, Firefox, Edge, Varsayılan (sistem) |
| Tür etiketleri | Program, Klasör, Belge, Web adresi |
| Düzenleme dialogu | Öğe Ekle / Öğeyi Düzenle, Ad, Tür, Yol / Adres, Gözat… |
| Hatalar | bulunamadı, açılamadı, tarayıcı bulunamadı, Kaydedilemedi |

**Çevrilmeyenler:** öğe adları (kullanıcının girdiği), dosya yolları,
uygulama adı "ReadytoWork".

### 4.4 Anında dil değişimi

`t()` aktif dili her çağrıda okur. Dil değişince combobox değerleri,
tüm buton metinleri ve etiketler `<<ComboboxSelected>>` olayıyla yeniden
yazılır. **Pencere kapatıp açmaya gerek yok.**

### 4.5 Eksik çeviri koruması

Test: `en.json`/`zh.json`/`de.json`/`it.json` içindeki her anahtar `tr.json`'da
bulunmalı. Yeni metin eklendiğinde eksik çeviri CI'da yakalanır.

---

## 5. Davranış değişiklikleri

### 5.1 İlk çalışma

`config.json` yoksa ayarlar penceresi **otomatik açılır** — kullanıcı boş
tepsi görüp nedenini anlamaz. Boş listeyle kaydetmek geçerlidir.
Aynı koşul bozuk dosya sonrası da geçerlidir: `.bak` oluştuğunda liste boş
döner ve pencere kullanıcıya yeniden düzenleme fırsatı verir.

### 5.2 Kaydedilmemiş değişiklik uyarısı

Pencere X ile kapatılırsa ve listede değişiklik varsa
`messagebox.askyesno("Kaydedilmemiş değişiklik var...")` sorulur.

### 5.3 Varsayılan öğeler kaldırıldı

`DEFAULT_ITEMS` tamamen silindi. Dünya çapında sürümde başkasının kişisel
tez yolu yanlış şey açmaya çalışmasın. Boş liste ile başlar.

### 5.4 Bozuk karakter düzeltmesi

`actions.py` içindeki `a����lamad��`, `bulunamad��`, `klas��r`, `Bilinmeyen
t��r` bozuk Türkçe karakterler düzeltilecek ve `t()` ile çevrilecek.

### 5.5 Türkçe karakter testi

`actions.py` ve diğer tüm kaynak dosyaları UTF-8 olarak okunabilir;
bozuk karakter taraması testte yapılır.

---

## 6. Paketleme

### 6.1 PyInstaller

Giriş noktası `v1.py` → `readytowork.py`. Spec `v1.spec` →
`ReadyToWork.spec`, çıktı `dist/ReadyToWork.exe`.
`version.py`'den sürüm okunur. `console=False`, ikon gömülü.

### 6.2 Inno Setup (`installer.iss`)

**Tamamı İngilizce** (kullanıcı talebi):

```
ReadyToWork Setup
  Welcome / License / Select Install Location / Ready to Install /
  Installing / Finish
Install dir : C:\Program Files\ReadyToWork   (değiştirilebilir)
Start Menu  : ReadyToWork klasörü + çalıştır/kaldır kısayolları
Desktop icon: onay kutusu (varsayılan işaretli)
Run at startup: onay kutusu (varsayılan işaretli) → registry Run kaydı
Uninstaller : hazırlanır, .bak dosyaları dahil
Uninstall   : %APPDATA%\ReadyToWork\ SİLİNİR
```

`Run` bölümü yok — kullanıcı kendi başlatır.

**İmzalama:** `SignTool` satırı hazır, kod imzalama sertifikası kullanıcıya ait.
İmzasız da derlenir (SmartScreen uyarısı verir).

### 6.3 Sürümleme

SemVer. İlk halka açık sürüm **`1.0.0`**.

---

## 7. GitHub

Repo: `github.com/ilkeryigit/ReadytoWork`, lisans **MIT**.
GitHub kimliği `ilkeryigit`; git commit yazarı olarak noreply adresi kullanılır
(gerçek e-posta hiçbir yere yazılmaz — bkz. §8).

| Alan | İçerik |
|---|---|
| Description | `Windows tray launcher — pin your programs, folders, documents and URLs. Ready in seconds, every morning.` |
| Topics (10) | `windows`, `tray`, `launcher`, `pystray`, `python`, `productivity`, `tkinter`, `windows-only`, `pyinstaller`, `open-source` |
| About → Websites | `github.com/ilkeryigit/ReadytoWork/releases` |
| README.md | Kurulum, ekran görüntüsü, kullanım, 5 dil, build, katkı, lisans + badge'ler |
| LICENSE | MIT — Copyright (c) 2026 ilkeryigit |
| CONTRIBUTING.md | Çeviri ekleme adımları (5 adım) |
| CODE_OF_CONDUCT.md | Contributor Covenant 2.1 |
| .github/ISSUE_TEMPLATE/ | `bug_report.yml`, `feature_request.yml` |
| .github/ | `PULL_REQUEST_TEMPLATE.md`, `workflows/release.yml` |
| CHANGELOG.md | Keep a Changelog + SemVer |

**`release.yml`:** tag push (`v1.0.0`) → Windows runner'da PyInstaller build →
Inno Setup ile `ReadyToWork-Setup-1.0.0.exe` → GitHub Release'e
**otomatik İngilizce release notları** ile yüklenir.

---

## 8. Gizlilik — public repo'da kişisel veri olmaz

**Bu bir P0 şarttır:** yayımlanan repo'da geliştiriciye ait hiçbir kişisel
bilgi bulunmaz.

### 8.1 Tespit edilen kişisel veri (temizlenecek)

| Yer | İçerik |
|---|---|
| `config.py` | `DEFAULT_ITEMS` içinde geliştirici masaüstü/tezyolu |
| eski plan + spec dosyaları | çalışma dizini ve kişisel belge yolları |
| eski git config | geliştiriciye ait yazar kimliği |
| **eski git blob'ları** | aynı yollar `git log -p` ile okunabilir |

### 8.2 Temiz git geçmişi (zorunlu)

Mevcut geçmiş **korunmaz.** Public repo, eski blob'ları taşımayan **tek bir
temiz kök commit** ile başlatılır (`git checkout --orphan` + `git commit`).
Böylece eski kullanıcı adı, kişisel belge yolları ve gerçek e-posta hiçbir
yerde görünmez.

Commit yazarı: `ilkeryigit <ilkeryigit@users.noreply.github.com>`
(repo-local `git config`, gerçek e-posta kullanılmaz).

### 8.3 Doküman kapsamı

Public repo'ya **yalnızca** bu spec girer. `docs/superpowers/plans/` ve
eski spec dosyaları public repoya **dahil edilmez** (yerelde kalır).

### 8.4 Otomatik denetim

`tests/test_privacy.py` public'a girecek dosyaları tarar ve **desen
tanımlarının kendisini tutan tek doğruluk kaynağıdır** (`PATTERNS` listesi).
Şunları arar:

- ev dizini yolu deseni (kullanıcı profil klasörü biçiminde mutlak yollar)
- eski geliştirici kullanıcı adı
- kişisel belge/tezyolu adları
- kişisel e-posta alan adları

Tarama kapsamı: kaynak dosyalar, `lang/`, `tests/`, `*.md`, `*.iss`, `*.spec`.
Hariç: `.venv`, `build`, `dist`, `.git`, ve **kendi desen tanımları satırları**
(kendini yakalamaması için).

### 8.5 Yayımlama öncesi kontrol listesi

1. `pytest tests` — `test_privacy.py` dahil yeşil
2. `git log --format='%an %ae' | sort -u` — sadece `ilkeryigit <noreply>`
3. `pytest tests/test_privacy.py -v` — desen listesi `PATTERNS`, kapsam §8.4
4. `gh repo create ilkeryigit/ReadytoWork --public --source . --push`

---

## 9. Test stratejisi

Mevcut 4 test dosyası korunur, yeni eklenenler:

| Test | Kapsam |
|---|---|
| `test_config.py` | atomik save, .tmp temizliği, bozuk JSON yedeği, geçersiz alanlar, legacy taşıma |
| `test_i18n.py` | t() fallback, 5 dil dosyası yükleme, eksik anahtar tespiti, aktif dil değişimi |
| `test_gui.py` | ilk çalışma açılışı, kaydedilmemiş değişiklik uyarısı, dil değişimi metin güncelleme |
| `test_actions.py` | t() ile hata mesajları, **bozuk karakter taraması** |
| `test_readytowork.py` | tek örnek mutex, sürüm okuma |
| `test_privacy.py` | **kişisel veri taraması** (bkz. §8.4) |

Dış OS çağrıları mock'lanır (`subprocess.Popen`, `os.startfile`,
`webbrowser.open`) — gerçek sistem çağrısı yapılmaz.

---

## 10. Kapsam dışı

- macOS / Linux desteği (Windows-only tasarım kasıtlı)
- Çeviriler için çeviri yönetim sitesi (Weblate vb.)
- Kod imzalama sertifikası satın alma
- Oto-updater (güncellemeler GitHub Releases üzerinden manuel)
- Kişisel veri temizliği dışında eski projeye geri dönüş desteği

---

## 11. Uygulama öncesi temizlik

Çalışan eski sürüm (`Desktop` altındaki eski exe) tray'den Çıkış ile
kapatılır ve silinir. Mevcut config.json **hiçbir yerde yok** →
veri kaybı yok.
