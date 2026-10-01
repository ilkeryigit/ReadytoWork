# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing yet.

## [1.0.0] - 2026-10-01

First public release. Previously distributed as "Doktora Başlatıcı".

### Added

- Five-language interface: English, Türkçe, 中文, Deutsch, Italiano, switchable
  from the settings window without a restart.
- Translation catalogs in `lang/*.json`; adding a language needs no code change.
- Inno Setup installer with Start Menu and desktop shortcuts, an optional
  start-with-Windows task, and an uninstaller that removes the settings folder.
- GitHub Actions release workflow that builds the executable and the installer
  and publishes both to a GitHub release with English notes.
- Automated privacy check in the test suite: the repository must not contain
  personal paths, usernames or email addresses.
- First run opens the settings window automatically.

### Fixed

- **Settings no longer revert.** The configuration file was written next to the
  executable, so two copies of the app each kept their own list and appeared to
  lose changes. It now lives in `%APPDATA%\ReadytoWork\config.json`.
- Settings are written atomically (temporary file plus rename). A crash, a full
  disk or a locked file can no longer leave a truncated configuration behind.
- Closing the settings window no longer reports success when the write failed.
  The window now stays open with an error, and unsaved changes prompt before
  closing.
- A corrupt configuration file is preserved as `config.json.bak` instead of
  being silently replaced.

### Changed

- Renamed from "Doktora Başlatıcı" to ReadytoWork.
- Configuration format uses English keys (`items`, `browser`, `lang`) and English
  type values (`program`, `folder`, `document`, `url`). Files written by older
  versions are still read and migrated automatically.
- All code identifiers are English.
- Removed the built-in default items: they contained personal document paths and
  were meaningless on any other machine.

### Removed

- Turkish-only interface.
- Default items containing personal paths.

[Unreleased]: https://github.com/ilkeryigit/ReadytoWork/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/ilkeryigit/ReadytoWork/releases/tag/v1.0.0
