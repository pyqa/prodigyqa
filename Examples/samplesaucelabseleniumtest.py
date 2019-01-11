"""Sample test scripts for saucelab pytest sample."""

from imgqa import BrowserActions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# Selenium 3.14+ doesn't enable certificate checking                
import urllib3                                                      
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

chrome_options = Options()
chrome_options.add_argument("--headless")


class Page:
    """hold all locators for POM style implementation."""

    base_url = "http://www.python.org"
    two_url = "https://xkcd.com/979/"
    search_box = {"locatorvalue": 'id-search-field',
                  "by": "By.ID", "value": "selenium " + Keys.ENTER}
    button = {"locatorvalue": '#topLeft > ul > li:nth-child(1) > a',
              "by": "By.CSS_SELECTOR"}
    desired_cap = {                   
    'platform': "Mac OS X 10.12", 
    'browserName': "chrome",      
    'version': "latest",          
    }   
    # Enter your sauce lab access credentials below.
    username = ''                                  
    access_key = ''  


class TestClass(BrowserActions):
    """Test Class Container for test cases."""

    def setUp(self):
        # Added the below line for configuring remote web driver.
        self.driver = webdriver.Remote(                                                                      
                command_executor='https://{}:{}@ondemand.saucelabs.com/wd/hub'.format(Page.username, Page.access_key), 
                desired_capabilities=Page.desired_cap)                                                            

    def tearDown(self):
        self.driver.quit()

    def test_python_search(self):
        """Sample case for navigating to python site and search selenium."""
        self.open(Page.base_url)
        self.set_window_size(1200, 800)
        self.maximize()
        self.assertIn("Python", self.get_title())
        self.click(Page.search_box)
        self.send_keys(Page.search_box)
        self.open(Page.two_url)
        self.click(Page.button)
