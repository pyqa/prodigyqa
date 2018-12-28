"""Sample test scripts for selenium pytest sample."""

from imgqa import BrowserActions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument("--headless")


class Page:
    """hold all locators for POM style implementation."""

    base_url = "http://www.python.org"
    search_box = {"locatorvalue": 'q',
                  "by": "By.XPATH", "value": "selenium"}


class TestClass(BrowserActions):
    """Test Class Container for test cases."""

    def test_python_search(self):
        """Sample case for navigating to python site and search selenium."""

        # Added the below line for travis to enable headless mode test
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.open(Page.base_url)
        self.maximize()
        self.assertIn("Python", self.get_title())
        self.send_keys(Page.search_box[locatorvalue], Page.search_box[value])
        self.send_keys(Keys.ENTER)
