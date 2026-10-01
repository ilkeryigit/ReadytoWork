"""Personal data must never reach the public repository.

The public repo is the whole tracked tree, so this scans every tracked file for
the kind of data that would identify the machine or the author.
"""
import pathlib
import re
import subprocess
import unittest

ROOT = pathlib.Path(__file__).parent.parent

# Windows user profile roots and any drive-lettered user folder.
PROFILE_PATTERNS = [
    r"[A-Za-z]:\\Users\\",
    r"[A-Za-z]:/Users/",
    r"\\\\Users\\",
]

# Standalone email addresses (setuptools-style excluded via the domain rule).
EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

# Allowed domain-like strings that are not mail addresses. The GitHub
# noreply domain is designed to be public: it is the commit author address.
EMAIL_ALLOWLIST = {
    "github.com",
    "users.noreply.github.com",
    "example.com",
    "contributor-covenant.org",
    "keepachangelog.com",
    "semver.org",
    "pyinstaller.org",
    "python.org",
    "en.wikipedia.org",
}

TEXT_SUFFIXES = {
    ".py", ".md", ".json", ".txt", ".yml", ".yaml", ".iss", ".spec",
    ".cfg", ".ini", ".toml", ".gitignore", ".example",
}

SKIP_DIRS = {
    ".git", ".venv", "build", "dist", "__pycache__", ".pytest_cache",
    ".superpowers", "graphify-out", ".github-cache",
}

# This file holds the patterns, so scanning it would always match.
SELF = pathlib.Path(__file__).name


def tracked_files():
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z", "--cached"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return [p for p in out.split("\0") if p]


def is_scannable(rel: str) -> bool:
    if any(part in SKIP_DIRS for part in pathlib.PurePosixPath(rel).parts):
        return False
    name = pathlib.PurePosixPath(rel).name
    if name == SELF:
        return False
    suffix = pathlib.PurePosixPath(rel).suffix.lower()
    return suffix in TEXT_SUFFIXES or name in TEXT_SUFFIXES


def scan(rel: str):
    path = ROOT / rel
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    findings = []
    for pattern in PROFILE_PATTERNS:
        for match in re.finditer(pattern, text):
            line_no = text.count("\n", 0, match.start()) + 1
            findings.append(f"{rel}:{line_no} profile path {match.group(0)!r}")
    for match in re.finditer(EMAIL_PATTERN, text):
        domain = match.group(0).rsplit("@", 1)[-1].lower()
        if domain in EMAIL_ALLOWLIST:
            continue
        line_no = text.count("\n", 0, match.start()) + 1
        findings.append(f"{rel}:{line_no} email {match.group(0)!r}")
    return findings


class PrivacyTests(unittest.TestCase):
    def test_tracked_files_have_no_personal_data(self):
        files = tracked_files()
        if files is None:
            self.skipTest("git not available")
        findings = []
        for rel in files:
            if is_scannable(rel):
                findings.extend(scan(rel))
        self.assertEqual(
            findings, [],
            "Personal data leaked into the repository:\n" + "\n".join(findings),
        )

    def test_no_os_specific_personal_defaults_in_source(self):
        for rel in ("config.py", "app.py", "gui.py", "actions.py", "readytowork.py"):
            findings = scan(rel)
            self.assertEqual(
                findings, [],
                f"Personal data in {rel}:\n" + "\n".join(findings),
            )
