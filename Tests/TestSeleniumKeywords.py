"""Sample test scripts for selenium pytest sample."""
import pytest
from imgqa import BrowserActions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from imgqa import browseractions
from proboscis.asserts import assert_true
import time
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument("--headless")

class PageObjects():
    """hold all locators for POM style implementation."""

    base_url = "https://learn.letskodeit.com/p/practice"
    two_url = "https://xkcd.com/979/"
    #  search_boxes = {{"locatorvalue": 'id-search-field',
    #               "by": "By.ID", "value": "selenium " + Keys.ENTER}}
    RadioButtons_all = {"bmwButton": {"locatorvalue": 'bmwradio',"by": "By.ID", "value": 'ch_signup_icon'},
                        "benzButton":{"locatorvalue": 'benzradio',"by": "By.ID", "value": 'ch_signup_icon'}}
    SelectButton1={"locatorvalue": 'carselect',"by": "By.ID", "value": 'benz'}
    SelectButton2 = {"locatorvalue": 'carselect', "by": "By.ID", "value": 'bmw'}
    checkBox_all = {"bmwbutton": {"locatorvalue": 'bmwcheck',"by": "By.ID", "value": 'bmw'},
                    'benzbutton':{"locatorvalue": 'benzcheck',"by": "By.ID", "value": 'bmw'}}
    buttons_all={"openwindow": {"locatorvalue": 'openwindow',"by": "By.ID", "value": 'openwindow'},
                 "alertBtn":{"locatorvalue": 'alertbtn',"by": "By.ID", "value": 'alertbtn'},
                 "confirmbtn":{"locatorvalue": 'confirmbtn',"by": "By.ID", "value": 'confirmbtn'},
                 "mousehover": {"locatorvalue": 'mousehover',"by": "By.ID", "value": 'mousehover'}}
    labels_all = {"footer": {"locatorvalue": 'powered-by', "by": "By.CLASS_NAME", "value": 'powered-by'},
                  "practice": {"locatorvalue": "/pages/practice", "by": "By.LINK_TEXT", "value": '/pages/practice'}}
    links_all = {'top_mousehover':{"locatorvalue": "#top","by": "By.LINK_TEXT", "value": '#top'}}

    text_boxes_all = {"search_text_box": {"locatorvalue": 'search-courses',
                                         "by": "By.ID", "value": "selenium" + Keys.ENTER},
                      "mobile_no_text_box": {"locatorvalue": 'ch_signup_phone',
                                             "by": "By.ID", "value": "9502668772" + Keys.ENTER},
                      "pwd_text_box": {"locatorvalue": 'ch_signup_password',
                                       "by": "By.ID", "value": "9502668772" + Keys.ENTER}}



class TestClass(BrowserActions):
    """Test Class Container for test cases."""

    # def setUp(self):
    #     # Added the below line for travis to enable headless mode test
    #     self.driver = self.driver(chrome_options=chrome_options)
    #     # pass
    #
    # def tearDown(self):
    #     self.driver.quit()


    def test_BrowserActions1(self):

        """Sample case for navigating to python site and search selenium."""
        self.open(PageObjects.base_url)
        self.page_readiness_wait()
        self.set_window_size(1200, 800)
        self.maximize()
        self.scroll_to_element(
            PageObjects.buttons_all.get("mousehover"))
        self.hover_on_element(
            PageObjects.buttons_all.get("mousehover"))
        self.wait_for_element(
            PageObjects.links_all.get("top_mousehover"))
        self.hover_on_click(
            PageObjects.links_all.get("top_mousehover"))
        self.wait_for_element(
            PageObjects.RadioButtons_all.get("benzButton"))
        self.title = self.get_title()
        self.drivername = self.get_driver_name()
        self.domainurl = self.get_domain_url()
        assert_true(str(self.drivername) ==
                    'chrome', 'driver name is not matched')
        assert_true(str(self.domainurl) ==
                    'https://learn.letskodeit.com', 'domain url is not matched')
        assert_true(str(self.title) == "Practice | Let's Kode It",
                    "Title is not matched with expected")
        self.pagesource = self.get_page_source()
        assert_true(
            self.pagesource.startswith("<!DOCTYPE html"),
                    "Page source is not returned")
        self.click(
            PageObjects.RadioButtons_all.get("benzButton"))
        self.click(
            PageObjects.RadioButtons_all.get("bmwButton"))
        self.locator_check(
            PageObjects.RadioButtons_all.get("benzButton"))
        assert_true(self.by_value == 'id', "locator check is not working")
        self.click(
            PageObjects.SelectButton1)
        self.select_option_by_value(
            PageObjects.SelectButton1, "honda")
        self.select_option_by_value(
            PageObjects.SelectButton1, "Honda")
        self.scroll_to_element(
            PageObjects.buttons_all.get('openwindow'))
        self.click(
            PageObjects.buttons_all.get('openwindow'))
        time.sleep(5)
        window_before = self.driver.window_handles[0]
        window_after = self.driver.window_handles[1]
        self.switch_to_window(window_after)
        self.reload_page()
        url = self.get_location()
        assert_true(url.startswith(
            "https://letskodeit.teachable.com/courses"),
                    "current location is not returned")
        self.reload_page()
        url = self.get_location()
        assert_true(url.startswith(
            "https://letskodeit.teachable.com/courses"),
                    "current location is not returned")
        self.driver.close()
        self.switch_to_window(window_before)
        self.driver.quit()

    def test_BrowserActions2(self):
        self.open(PageObjects.base_url)
        self.page_readiness_wait()
        self.set_window_size(1200, 800)
        self.maximize()
        self.click(PageObjects.buttons_all.get('alertBtn'))
        time.sleep(3)
        self.switch_to_alert()
        self.wait_and_accept_alert()
        time.sleep(3)
        self.click(PageObjects.buttons_all.get('confirmbtn'))
        time.sleep(3)
        self.switch_to_alert()
        self.wait_and_reject_alert()
        self.switch_to_frame("iframe-name")
        self.scroll_to_element(
            PageObjects.text_boxes_all.get('search_text_box'))
        self.send_keys(
            PageObjects.text_boxes_all.get('search_text_box'))
        time.sleep(5)
        self.clear_text(
            PageObjects.text_boxes_all.get('search_text_box'))
        time.sleep(5)
        text=self.get_text(
            PageObjects.text_boxes_all.get('search_text_box'))
        self.switch_to_default_content()
        self.scroll_to_footer()
        time.sleep(6)
        self.open("https://learn.letskodeit.com/courses")
        assert_true(
            self.get_location()=='https://learn.letskodeit.com/courses',
            "Didnot hit the courses page")
        self.go_back()
        assert_true(self.get_location()
                    == 'https://learn.letskodeit.com/p/practice',
                    "go back is not working")
        self.go_forward()
        assert_true(self.get_location()
                    == 'https://learn.letskodeit.com/courses',
                    "go forward is not working")
        self.go_back()
        time.sleep(5)
        self.capture_screenshot(
            "C:\\Users\\pramati\\Desktop\\Screenshots\\exampleScreenshot1.png")
        self.switch_to_active_element()