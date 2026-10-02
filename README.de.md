# ReadytoWork

**Ein Windows-Tray-Launcher: Programme, Ordner, Dokumente und Webadressen
mit einem Klick erreichbar.**

[English](README.md) · [Türkçe](README.tr.md) · [中文](README.zh.md) · [Deutsch](README.de.md) · [Italiano](README.it.md)

---

## Wozu?

Jeden Morgen öffnen Sie dieselben paar Dinge: ein Dokument, an dem Sie
schreiben, einen Literaturverwalter, einen Ordner mit Quellen, ein Dashboard.
ReadytoWork hält sie in einem Tray-Menü – ein Klick statt der Suche im
Startmenü und auf dem Desktop.

Ein kleines, ehrliches Werkzeug: kein Konto, keine Cloud, keine Telemetrie, kein
Netzwerkverkehr im Hintergrund. Ihre Liste liegt in einer einzigen JSON-Datei auf
Ihrem eigenen Rechner.

## Funktionen

- **Tray-Menü** — alle Einträge aufgelistet, dazu *Alle öffnen* für den
  Ein-Klick-Morgen
- **Vier Eintragstypen** — Programm, Ordner, Dokument, Webadresse
- **Fünf Sprachen** — English, Türkçe, 中文, Deutsch, Italiano; jederzeit
  umschaltbar
- **Einstellungen, die bleiben** — gespeichert unter
  `%APPDATA%\ReadytoWork\config.json`, atomar geschrieben: ein Absturz oder eine
  volle Festplatte kann sie nicht beschädigen
- **Sortieren und umbenennen** — Einträge verschieben, direkt bearbeiten
- **Browserwahl** — Webadressen im Standardbrowser, in Chrome, Firefox oder Edge
  öffnen
- **Einzelinstanz** — ein zweiter Start tut nichts; nichts stapelt sich
- **Nativer Installer** — Startmenü- und Desktop-Verknüpfungen, optionaler
  Autostart, Deinstallationsprogramm

## Installation

Laden Sie den Installer von der [Releases-Seite](https://github.com/ilkeryigit/ReadytoWork/releases),
führen Sie `ReadytoWork-Setup-1.0.0.exe` aus und wählen Sie Ihre Optionen.

> Der Installer ist nicht signiert, daher kann Windows SmartScreen beim ersten
> Start warnen. Wählen Sie *Weitere Informationen → Trotzdem ausführen*.

## Verwendung

1. Starten Sie ReadytoWork. Beim ersten Start öffnet sich automatisch das
   Einstellungsfenster.
2. **Hinzufügen**, Typ wählen, Namen vergeben, Pfad auswählen oder Adresse
   einfügen.
3. **Speichern**. Der Eintrag liegt jetzt im Tray-Menü.
4. Rechtsklick auf das Tray-Symbol → *Alle öffnen*.

Beim Deinstallieren werden die Einstellungen entfernt.

## Aus dem Quelltext bauen

Erfordert Python 3.10+ unter Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# aus dem Quelltext starten
.\.venv\Scripts\python.exe readytowork.py

# Tests
.\.venv\Scripts\python.exe -m pytest tests -v

# einzelne ausführbare Datei -> dist\ReadytoWork.exe
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm ReadytoWork.spec

# Installer -> dist\ReadytoWork-Setup-1.0.0.exe   (benötigt Inno Setup 6)
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" installer.iss
```

## Übersetzen

Alle sichtbaren Texte liegen in `lang/<code>.json`. Die Schritte für eine neue
Sprache stehen in [CONTRIBUTING.md](CONTRIBUTING.md).

## Mitwirken

Beiträge sind willkommen – Fehlerberichte, Übersetzungen und kleine
Funktionen helfen alle. Das ist ein reines Windows-Werkzeug ohne
Laufzeitabhängigkeiten außer `pystray` und `Pillow`, und daran halten wir uns.

- **Fehler und Ideen:** ein Issue öffnen. Bitte vorher offene Issues prüfen.
- **Kleine Korrekturen und Übersetzungen:** Issues mit dem Label
  [`good first issue`](https://github.com/ilkeryigit/ReadytoWork/labels/good%20first%20issue)
  ansehen – sie sind bewusst klein gefasst.
- **Größere Änderungen:** bitte zuerst ein Issue öffnen, damit wir die
  Vorgehensweise abstimmen können.

Einrichtung, Grundregeln und eine Anleitung zum Hinzufügen einer Sprache stehen in
[CONTRIBUTING.md](CONTRIBUTING.md). Für alle Mitwirkenden gilt der
[Verhaltenskodex](CODE_OF_CONDUCT.md).

## Datenschutz

Keine Analysen, keine Netzwerkaufrufe, kein Tracking. Die einzige Datei außerhalb
des Installationsverzeichnisses ist `%APPDATA%\ReadytoWork\config.json` mit den
von Ihnen angelegten Einträgen. Die Testsuite enthält eine automatische Prüfung,
dass keine persönlichen Pfade, Benutzernamen oder E-Mail-Adressen ins Repository
gelangen.

## Lizenz

[MIT](LICENSE) © 2026 ilkeryigit