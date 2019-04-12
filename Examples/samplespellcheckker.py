"""Sample test scripts for selenium pytest sample."""

from prodigy.utils import Utilities


class PageObjects:
    """hold all locators for POM style implementation."""

    url = "https://reqres.in/"
    custom_words = ["jQuery", "GIFs", "Uptime", "XMLHttpRequest",
                    "ga", "Req", "Pantone", "paul", "ie",
                    "createdAt", "backend", "Reqres", "opentype",
                    "SVGs", "Howdle", "lt", "https", "JSBin",
                    "rudd", "woff", "CORS", "CSS", "src",
                    "Sailsjs", "url", "xhr", "JSFiddle"]


class TestClass(Utilities):
    """Test Class Container for test cases."""

    def test_spell_checker(self):
        """Sample test suite."""
        # misspelled = self.spell_checker(PageObjects.url)
        # self.assertEqual(sorted(misspelled),
        #                  sorted(PageObjects.custom_words))
        pass
