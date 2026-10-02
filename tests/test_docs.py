"""The public docs must not link to files that do not exist."""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).parent.parent

READMES = [
    "README.md",
    "README.tr.md",
    "README.zh.md",
    "README.de.md",
    "README.it.md",
]

LINK_PATTERN = re.compile(r"\]\(([^)#]+)\)")


class ReadmeTests(unittest.TestCase):
    def test_readmes_exist(self):
        for name in READMES:
            self.assertTrue((ROOT / name).exists(), f"missing {name}")

    def test_local_links_resolve(self):
        broken = []
        for name in READMES:
            text = (ROOT / name).read_text(encoding="utf-8")
            for link in LINK_PATTERN.findall(text):
                if link.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (ROOT / link).exists():
                    broken.append(f"{name} -> {link}")
        self.assertEqual(broken, [], "broken links: " + ", ".join(broken))

    def test_artifact_names_match_the_build(self):
        """README, CI and the installer must agree on the produced file names."""
        spec = (ROOT / "ReadytoWork.spec").read_text(encoding="utf-8")
        self.assertIn('name="ReadytoWork"', spec)

        iss = (ROOT / "installer.iss").read_text(encoding="utf-8")
        self.assertIn('#define AppExeName "ReadytoWork.exe"', iss)

        # OutputBaseFilename uses {#AppName}-Setup-{#AppVersion}
        app_name = re.search(r'#define AppName "([^"]+)"', iss).group(1)
        version = re.search(r'#define AppVersion "([^"]+)"', iss).group(1)
        expected = f"{app_name}-Setup-{version}.exe"
        self.assertIn(expected, (ROOT / "README.md").read_text(encoding="utf-8"))

        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn(f"dist/{app_name}-Setup-*.exe", workflow)
        self.assertIn(f"dist/{app_name}.exe", workflow)