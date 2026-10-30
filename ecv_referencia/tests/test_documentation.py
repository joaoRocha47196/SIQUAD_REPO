"""The generated parts of the documentation: the Markdown blocks match the example declarations, and the site
has no broken links."""
import re
import tempfile
import unittest
from pathlib import Path

from ecv.tools.documentation import generate
from ecv.tools.readme_blocks import stale


class TestDocumentation(unittest.TestCase):
    def test_generated_blocks_are_current(self):
        self.assertEqual(stale(), [], "python -m ecv docs")

    def test_site_has_no_broken_links(self):
        with tempfile.TemporaryDirectory() as d:
            folder, n = generate(Path(d) / "site")
            self.assertGreater(n, 100)
            pages = {p.name for p in folder.glob("*.html")}
            for p in folder.glob("*.html"):
                for href in re.findall(r'href="([^"#?]+\.html)', p.read_text(encoding="utf-8")):
                    if "/" not in href and not href.startswith("http"):
                        self.assertIn(href, pages, f"{p.name} → {href}")


if __name__ == "__main__":
    unittest.main()
