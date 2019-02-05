"""REST Api Sample Test file."""

from imgqa import Webspider
from selenium.webdriver.common.keys import Keys

username = {"locatorvalue": "id-search-field",
            "by": "By.ID",
            "value": "username" + Keys.ENTER}
password = {"locatorvalue": 'id-search-field',
            "by": "By.ID",
            "value": "password" + Keys.ENTER}
login_button = {"locatorvalue": "login-button",
                "by": "By.ID"}

baseurl = "http://the-internet.herokuapp.com/"


class TestClass(Webspider):
    """Sample Test Suite."""

    # def test_get_web_urls1(self):
    #     """Get web urls using selenium from application."""
    #     self.spider(baseurl, login=True)

    def test_get_web_urls2(self):
        """Get web urls using scrapy from application."""
        self.spider(baseurl, login=False)
