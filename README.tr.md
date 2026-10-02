# ReadytoWork

**Windows tepsi başlatıcısı: programlarınız, klasörleriniz, belgeleriniz ve
adresleriniz tek tıkla erişime açık olsun.**

[English](README.md) · [Türkçe](README.tr.md) · [中文](README.zh.md) · [Deutsch](README.de.md) · [Italiano](README.it.md)

---

## Neden?

Her sabah aynı birkaç şeyi açıyorsunuz: yazdığınız bir belge, bir referans
yöneticisi, kaynak dosyalarınızın bulunduğu klasör, bir panel. ReadytoWork
bunları tek bir tepsi menüsünde tutar; böylece Başlat menüsünde ve masaüstünde
arama yapmak yerine hepsini tek tıkla açarsınız.

Küçük ve dürüst bir araç: hesap yok, bulut yok, telemetri yok, arka planda ağ
trafiği yok. Listeniz tek bir JSON dosyasında, kendi makinenizde durur.

## Özellikler

- **Tepsi menüsü** — tüm öğeler listelenir, ayrıca hepsini tek tıkla açan
  *Tümünü aç*
- **Dört öğe türü** — program, klasör, belge, web adresi
- **Beş dil** — İngilizce, Türkçe, 中文, Deutsch, Italiano; istediğiniz an
  değiştirilir
- **Kalıcı ayarlar** — `%APPDATA%\ReadytoWork\config.json` içinde, atomik
  yazılır; böylece bir çökme veya dolu disk ayarları bozamaz
- **Sırala ve yeniden adlandır** — öğeleri yukarı aşağı taşıyın, satır içi düzenleyin
- **Tarayıcı seçimi** — web adreslerini sistem varsayılanında, Chrome, Firefox
  veya Edge'de açın
- **Tek örnek** — iki kez başlatmak hiçbir şey yapmaz, uygulama yığınlaşmaz
- **Doğal kurulum sihirbazı** — Başlat menüsü ve masaüstü kısayolları, isteğe
  bağlı Windows ile başlatma, ayarları temizleyen kaldırıcı

## Kurulum

[Releases sayfasından](https://github.com/ilkeryigit/ReadytoWork/releases)
kurulum dosyasını indirin, `ReadytoWork-Setup-1.0.0.exe` dosyasını çalıştırın
ve seçeneklerinizi işaretleyin.

> Kurulum dosyası kod imzalı değildir; ilk çalıştırmada Windows SmartScreen
> uyarı verebilir. *Daha fazla bilgi → Yine de çalıştır* seçin.

## Kullanım

1. ReadytoWork'u başlatın. İlk açılışta ayarlar penceresi otomatik açılır.
2. **Ekle**'ye basın, tür seçin, bir ad verin ve bir yol seçin (ya da bir adres yapıştırın).
3. **Kaydet**'e basın. Öğe artık tepsi menünüzdedir.
4. Tepsi simgesine sağ tıklayın → hepsini açmak için *Tümünü aç*.

Ayarlar, uygulamayı kaldırdığınızda silinir.

## Kaynaktan derleme

Windows'ta Python 3.10+ gerekir.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# kaynaktan çalıştır
.\.venv\Scripts\python.exe readytowork.py

# testler
.\.venv\Scripts\python.exe -m pytest tests -v

# tek dosyalık çalıştırılabilir -> dist\ReadytoWork.exe
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm ReadytoWork.spec

# kurulum dosyası -> dist\ReadytoWork-Setup-1.0.0.exe   (Inno Setup 6 gerekir)
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" installer.iss
```

## Çeviri

Kullanıcıya görünen her metin `lang/<kod>.json` içindedir. Yeni bir dil eklemek
için `CONTRIBUTING.md` dosyasındaki adımları izleyin.

## Gizlilik

Analitik yok, ağ çağrısı yok, kullanıcı takibi yok. Kurulum dizini dışında
yazılan tek dosya, sizin oluşturduğunuz öğeleri tutan
`%APPDATA%\ReadytoWork\config.json` dosyasıdır. Test paketinde, deponun
içine kişisel yol, kullanıcı adı veya e-posta adresi sızmadığını doğrulayan
otomatik bir denetim vardır.

## Lisans

[MIT](LICENSE) © 2026 ilkeryigit