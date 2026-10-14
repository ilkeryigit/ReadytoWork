# ReadytoWork

**Un lanceur d'applications dans la barre d'état système de Windows qui vous
permet d'accéder à vos programmes, dossiers, documents et URL en un seul clic.**

[English](README.md) · [Türkçe](README.tr.md) · [中文](README.zh.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Français](README.fr.md)

---

## Pour qui ?

Doctorants, étudiants en master, étudiants universitaires et employés de
bureau — en bref, tous ceux dont la journée de travail commence par ouvrir les
mêmes outils.

## Pourquoi ?

Chaque matin, ouvrez-vous des dizaines de fichiers, de programmes et d'URL
simplement pour vous mettre au travail ? Les minutes perdues à fouiller dans
le menu Démarrer et sur votre bureau s'accumulent-elles, nuisent-elles à votre
concentration et vous font-elles perdre un temps précieux ?

Si la réponse est oui, cet outil est fait pour vous. Un seul clic suffit pour
tout ouvrir d'un coup, vous permettant ainsi d'être prêt à travailler sans
avoir à rassembler vos outils — et vous cessez de perdre du temps au début de
chaque journée.

C'est un petit outil simple : pas de compte, pas de cloud, pas de télémétrie,
pas de trafic réseau en arrière-plan. Votre liste est stockée dans un seul
fichier JSON sur votre propre ordinateur.


## Fonctionnalités

- **Menu de la barre d'état système** — tous les éléments répertoriés, plus l'option
  *Tout ouvrir* pour démarrer la journée en un clic
- **Quatre types d'éléments** — programme, dossier, document, adresse Web
- **Six langues** — English, Türkçe, 中文, Deutsch, Italiano, Français ; 
  modifiables à tout moment
- **Paramètres persistants** — stockés dans `%APPDATA%\ReadytoWork\config.json`,
  enregistrés de manière atomique afin qu'un plantage ou un disque plein ne
  puisse jamais les corrompre
- **Réorganiser et renommer** — déplacer les éléments vers le haut ou vers le
  bas, les modifier directement dans la liste
- **Choix du navigateur** — ouvrir les adresses Web dans le navigateur par
  défaut du système, Chrome, Firefox ou Edge
- **Instance unique** — le lancer deux fois ne change rien ; les instances ne
  s'accumulent jamais
- **Programme d'installation natif** — raccourcis dans le menu Démarrer et sur
  le bureau, démarrage avec Windows en option, programme de désinstallation
  propre

## Installation

Télécharger le programme d'installation depuis la [page des versions](https://github.com/ilkeryigit/ReadytoWork/releases),
lancer `ReadytoWork-Setup-1.0.1.exe`, puis choisir vos options.

> Le programme d'installation n'est pas signé numériquement ; Windows SmartScreen
  pourrait donc vous afficher un avertissement lors de la première
> exécution. Choisir *Plus d'informations → Exécuter quand même*.

## Utilisation

1. Lancer ReadytoWork. Au premier démarrage, la fenêtre des paramètres
   s'ouvre automatiquement.
2. Appuyer sur **Ajouter**, choisir un type, lui donner un nom et sélectionner
   un chemin d'accès (ou coller une URL).
3. Appuyer sur **Enregistrer**. L'élément apparaît désormais dans votre menu de
   la barre d'état système.
4. Clic droit sur l'icône de la barre d'état système → **Tout ouvrir** pour lancer 
   tous les éléments en même temps.

Les paramètres sont supprimés lorsque vous désinstallez l'application.

## Compilation à partir du code source

Nécessite Python 3.10 ou une version ultérieure sous Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Exécution à partir du code source
.\.venv\Scripts\python.exe readytowork.py

# Tests
.\.venv\Scripts\python.exe -m pytest tests -v

# Fichier exécutable autonome -> dist\ReadytoWork.exe
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm ReadytoWork.spec

# Programme d'installation -> dist\ReadytoWork-Setup-1.0.1.exe   (nécessite Inno Setup 6)
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" installer.iss
```

## Traduction

Chaque texte visible se trouve dans `lang/<code>.json`. Les étapes à suivre pour
ajouter une langue sont décrites dans [CONTRIBUTING.md](CONTRIBUTING.md).

## Contribuer

Les contributions sont les bienvenues : signalements de bugs, traductions et
petites fonctionnalités aident tout le monde. Il s'agit d'un outil
exclusivement destiné à Windows, sans dépendances d'exécution autres que
`pystray` et `Pillow`, et nous avons l'intention de le garder ainsi.

- **Bugs et idées :** ouvrez un ticket. Vérifiez d'abord ceux qui sont déjà
  ouverts.
- **Corrections et petites traductions :** consultez les tickets portant le
  label [`good first issue`](https://github.com/ilkeryigit/ReadytoWork/labels/good%20first%20issue)
  – leur portée est volontairement limitée.
- **Modifications plus importantes :** ouvrez d'abord un ticket, afin que nous
  puissions nous mettre d’accord sur la marche à suivre avant que vous
  n’écriviez le code.

Consultez le fichier [CONTRIBUTING.md](CONTRIBUTING.md) pour connaître les 
étapes de configuration, les règles de base et le guide d'ajout d'une langue. 
Les contributeurs sont tenus de respecter le [Code de conduite](CODE_OF_CONDUCT.md).

## Confidentialité

Aucune analyse, aucun appel réseau, aucun suivi. Le seul fichier
enregistré en dehors du répertoire d'installation est
`%APPDATA%\ReadytoWork\config.json`, qui contient les entrées que vous avez
créées. La suite de tests comprend une vérification automatique qui s'assure
qu'aucun chemin d'accès personnel, nom d'utilisateur ou adresse e-mail ne se
retrouve dans le référentiel.

## Licence

[MIT](LICENSE) © 2026 ilkeryigit
