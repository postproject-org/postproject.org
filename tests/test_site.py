import re
from html.parser import HTMLParser
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.stylesheets = []
        self.images = []
        self.icons = []
        self.scripts = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a":
            self.links.append(values.get("href"))
        if tag == "link" and values.get("rel") == "stylesheet":
            self.stylesheets.append(values.get("href"))
        if tag == "script":
            self.scripts.append(values.get("src"))
        if tag == "img":
            self.images.append(values.get("src"))
        if tag == "link" and values.get("rel") == "icon":
            self.icons.append(values.get("href"))


class SiteTest(TestCase):
    def setUp(self):
        self.source = (ROOT / "index.html").read_text(encoding="utf-8")
        self.parser = PageParser()
        self.parser.feed(self.source)

    def test_local_assets_exist(self):
        for asset in self.parser.stylesheets + self.parser.images + self.parser.icons + self.parser.scripts:
            self.assertTrue((ROOT / asset).is_file(), asset)
        for stylesheet in self.parser.stylesheets:
            stylesheet_path = ROOT / stylesheet
            source = stylesheet_path.read_text(encoding="utf-8")
            for asset in re.findall(r"url\(['\"]?([^)'\"\s]+)", source):
                self.assertTrue((stylesheet_path.parent / asset).is_file(), asset)

    def test_primary_destinations_are_secure(self):
        external = [
            link for link in self.parser.links
            if link != "/" and not link.startswith("#")
        ]
        for link in self.parser.links:
            if link.startswith("#"):
                self.assertIn(link[1:], self.parser.ids, link)
        self.assertTrue(external)
        self.assertTrue(all(link.startswith("https://") for link in external))

    def test_custom_domain_matches_landing_link(self):
        self.assertEqual((ROOT / "CNAME").read_text().strip(), "www.postproject.org")
        self.assertIn("https://docs.postproject.org/", self.parser.links)
