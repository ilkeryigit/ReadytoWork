# ReadytoWork

**Un launcher per la barra di sistema su Windows: programmi, cartelle, documenti
e indirizzi a portata di un clic.**

[English](README.md) · [Türkçe](README.tr.md) · [中文](README.zh.md) · [Deutsch](README.de.md) · [Italiano](README.it.md)

---

## Perché?

Ogni mattina apri le stesse cose: il documento in cui stai scrivendo, il gestore
di riferimenti, la cartella delle fonti, un cruscotto. ReadytoWork le tiene in un
unico menu di sistema, così le apri tutte con un clic invece di cercarle nel menu
Avvio e sul desktop.

È uno strumento piccolo e onesto: nessun account, nessun cloud, nessuna
telemetria, nessun traffico di rete in background. La tua lista sta in un solo
file JSON, sulla tua macchina.

## Funzionalità

- **Menu di sistema** — tutte le voci elencate, più *Apri tutto* per la mattina
  con un unico clic
- **Quattro tipi di voce** — programma, cartella, documento, indirizzo web
- **Cinque lingue** — English, Türkçe, 中文, Deutsch, Italiano; si cambia quando
  vuoi
- **Impostazioni che restano** — salvate in
  `%APPDATA%\ReadytoWork\config.json`, scritte in modo atomico: un arresto
  anomalo o un disco pieno non possono corromperle
- **Riordina e rinomina** — sposta le voci su e giù, modificalele sul posto
- **Scelta del browser** — apri gli indirizzi nel browser predefinito, in Chrome,
  Firefox o Edge
- **Istanza singola** — avviarlo due volte non fa nulla; non si accumula
- **Installer nativo** — collegamenti nel menu Start e sul desktop, avvio
  automatico facoltativo, disinstallazione che rimuove le impostazioni

## Installazione

Scarica l'installer dalla [pagina delle release](https://github.com/ilkeryigit/ReadytoWork/releases),
esegui `ReadytoWork-Setup-1.0.0.exe` e scegli le opzioni.

> L'installer non è firmato, quindi Windows SmartScreen potrebbe avvisarti alla
> prima esecuzione. Scegli *Ulteriori informazioni → Esegui comunque*.

## Utilizzo

1. Avvia ReadytoWork. Al primo avvio la finestra delle impostazioni si apre da
   sola.
2. Premi **Aggiungi**, scegli il tipo, assegna un nome e seleziona un percorso
   (o incolla un indirizzo).
3. Premi **Salva**. La voce è ora nel menu di sistema.
4. Tasto destro sull'icona → *Apri tutto*.

Le impostazioni vengono rimosse quando disinstalli l'applicazione.

## Compilare dal sorgente

Richiede Python 3.10+ su Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# esegui dal sorgente
.\.venv\Scripts\python.exe readytowork.py

# test
.\.venv\Scripts\python.exe -m pytest tests -v

# eseguibile in un unico file -> dist\ReadytoWork.exe
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm ReadytoWork.spec

# installer -> dist\ReadytoWork-Setup-1.0.0.exe   (richiede Inno Setup 6)
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" installer.iss
```

## Traduzione

Ogni testo visibile si trova in `lang/<codice>.json`. I passaggi per aggiungere
una lingua sono in [CONTRIBUTING.md](CONTRIBUTING.md).

## Privacy

Nessuna analisi, nessuna chiamata di rete, nessun tracciamento. L'unico file
scritto fuori dalla directory di installazione è
`%APPDATA%\ReadytoWork\config.json`, che contiene le voci che hai creato. La
suite di test include un controllo automatico che verifica che nel repository non
finiscano percorsi personali, nomi utente o indirizzi email.

## Licenza

[MIT](LICENSE) © 2026 ilkeryigit