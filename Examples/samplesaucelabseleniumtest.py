"""Sample test scripts for saucelab-python integration."""

import pytest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from prodigyqa import BrowserActions


class Page:

    base_url = "http://www.python.org"
    fb_base_url = "http://www.facebook.com"
    two_url = "https://xkcd.com/979/"
    search_box = {"locatorvalue": 'id-search-field',
                  "by": "By.ID", "value": "selenium " + Keys.ENTER}
    button = {"locatorvalue": '#topLeft > ul > li:nth-child(1) > a',
              "by": "By.CSS_SELECTOR"}
    # Use your sauce lab credentials.
    username = ''
    access_key = ''
    desired_cap = {
        'platform': "Mac OS X 10.12",
        'browserName': "chrome",
        'version': "latest",
    }


@pytest.fixture(scope="class")
def setup_teardown_fixture(request):
    """Fixture for class level setup and teardown methods.

    :param request: request for a particular functionality.
    :return: NA
    :rtype: NA
    """

    class Setup_Teardown(BrowserActions):
        def __init__(self):
            """Configuring remote web driver.

            :param: NA
            :return: NA
            :rtype: NA
            """
            self.driver = webdriver.Remote(
                command_executor='https://{}:{}@ondemand.saucelabs.'
                                 'com/wd/hub'.format(Page.username,
                                                     Page.access_key),
                desired_capabilities=Page.desired_cap)

    request.cls.st = Setup_Teardown()
    yield
    request.cls.st.driver.quit()


@pytest.mark.usefixtures("setup_teardown_fixture")
class TestClass():

    def test_python_search(self):
        self.st.open(Page.base_url)
        self.st.set_window_size(1200, 800)
        self.st.maximize()
        self.st.assertIn("Python", self.st.get_title())
        self.st.click(Page.search_box)
        self.st.send_keys(Page.search_box)
        self.st.open(Page.two_url)
        self.st.click(Page.button)

    def test_facebook_search(self):
        self.st.open(Page.fb_base_url)
        self.st.set_window_size(1200, 800)
        self.st.maximize()
        self.st.assertIn("Facebook", self.st.get_title())
