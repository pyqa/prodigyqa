"""Sample test scripts for selenium pytest sample."""

from imgqa import BrowserActions
import os
from selenium.webdriver.chrome.options import Options
from time import sleep

chrome_options = Options()


class PageObjects:
    """hold all locators for POM style implementation."""

    base_url = "http://the-internet.herokuapp.com/"
    base_url_title = "The Internet"
    bank_site_url = "https://www.icicidirect.com"
    RadioButtons_all = \
        {"bmwButton": {"locatorvalue": 'bmwradio',
                       "by": "By.ID",
                       "value": 'ch_signup_icon'},
         "benzButton":
             {"locatorvalue": 'benzradio',
              "by": "By.ID",
              "value": 'ch_signup_icon'}}
    SelectButton1 = {"locatorvalue": 'carselect',
                     "by": "By.ID", "value": 'benz'}
    SelectButton2 = {"locatorvalue": 'carselect',
                     "by": "By.ID", "value": 'bmw'}
    checkBox_all = {
        "checkbox1":
            {"locatorvalue": 'input[type="checkbox"]:nth-child(1)',
             "by": "By.CSS_SELECTOR",
             "value": '#checkboxes > input[type="checkbox"]:nth-child(1)'}
    }
    buttons_all = {
        "dropdown": {"locatorvalue": 'dropdown',
                     "by": "By.ID", "value": 'openwindow'},
        "option1": {
            "locatorvalue": '#dropdown > option:nth-child(2)',
            "by": "By.CSS_SELECTOR", "value": '1'},
        "option2": {
            "locatorvalue": '#dropdown > option:nth-child(3)',
            "by": "By.CSS_SELECTOR", "value": '2'},
        "mousehover": {"locatorvalue": 'mousehover', "by": "By.ID",
                       "value": 'mousehover'},
        'js_alert': {
            "locatorvalue": '#content > div > ul > li:nth-child(1) > button',
            "by": "By.CSS_SELECTOR",
            "value": '#content > div > ul > li:nth-child(1) > button'},
        'js_confirm_alert': {
            "locatorvalue": '#content > div > ul > li:nth-child(2) > button',
            "by": "By.CSS_SELECTOR",
            "value": '#content > div > ul > li:nth-child(2) > button'},
        'js_prompt_alert': {
            "locatorvalue": '#content > div > ul > li:nth-child(3) > button',
            "by": "By.CSS_SELECTOR",
            "value": '#content > div > ul > li:nth-child(3) > button'},
        'enable_btn': {
            'locatorvalue': '#input-example > button',
            'by': 'By.CSS_SELECTOR', 'value': 'test'}
    }
    labels_all = {
        "header": {
            "locatorvalue": '.large-12.columns.atom.text-center>h1',
            "by": "By.CSS_SELECTOR",
            "value": '.large-12.columns.atom.text-center>h1'},
        "practice": {
            "locatorvalue": "/pages/practice",
            "by": "By.LINK_TEXT", "value": '/pages/practice'}}
    links_all = {
        'checkboxes': {
            "locatorvalue": "#content > ul > li:nth-child(5) > a",
            "by": "By.CSS_SELECTOR",
            "value": '#content > ul > li:nth-child(5) > a'},
        'page_footer': {"locatorvalue": "#page-footer > div > div > a",
                        "by": "By.CSS_SELECTOR",
                        "value": '#page-footer > div > div > a'},
        'dropdown': {
            "locatorvalue": "/dropdown",
            "by": "By.LINK_TEXT", "value": '/dropdown'},
        'alerts': {
            "locatorvalue": "#content > ul > li:nth-child(25) > a",
            "by": "By.CSS_SELECTOR",
            "value": '#content > ul > li:nth-child(25) > a'},
        'frames': {
            "locatorvalue": "#content > ul > li:nth-child(19) > a",
            "by": "By.CSS_SELECTOR",
            "value": '#content > ul > li:nth-child(19) > a'},
        'iframe': {
            "locatorvalue": "#content > div > ul > li:nth-child(2) > a",
            "by": "By.CSS_SELECTOR",
            "value": '#content > div > ul > li:nth-child(2) > a'},
        'dynamic_controls': {
            "locatorvalue": "#content > ul > li:nth-child(11) > a",
            "by": "By.CSS_SELECTOR",
            "value": '#content > ul > li:nth-child(11) > a'}}
    text_boxes = {
        'text_in_frame': {
            "locatorvalue": "#tinymce > p", "by": "By.CSS_SELECTOR",
            "value": 'test message'},
        'text_box': {
            'locatorvalue': '#input-example > input',
            'by': 'By.CSS_SELECTOR', 'value': 'test'}}


class TestClass(BrowserActions):
    """Test Class Container for test cases."""

    def test_browser_actions(self):
        """Sample case for navigating to python site and search selenium."""
        self.open(PageObjects.base_url)
        self.page_readiness_wait()
        self.set_window_size(1200, 800)
        self.maximize()
        self.assertTrue(str(self.driver_name), 'chrome')
        self.assertTrue(str(self.domain_url), PageObjects.base_url)
        self.assertTrue(str(self.title), "The Internet")
        self.assertTrue(self.get_page_source().startswith("<!DOCTYPE html"))
        self.locator_check(
            PageObjects.links_all.get("page_footer"))
        self.assertTrue(self.by_value, 'css selector')
        self.scroll_to_footer()
        self.hover_on_element(
            PageObjects.links_all.get("page_footer"))
        self.wait_for_element(
            PageObjects.links_all.get("page_footer"))
        self.hover_on_click(
            PageObjects.links_all.get("page_footer"))
        window_before = self.driver.window_handles[0]
        window_after = self.driver.window_handles[1]
        self.switch_to_window(window_after)
        self.reload_page()
        url = self.get_location()
        self.assertTrue(url.startswith("http://elementalselenium.com/"))
        text = self.get_text(PageObjects.labels_all.get('header'))
        self.assertTrue(str(text), 'Elemental Selenium')
        self.driver.close()
        self.switch_to_window(window_before)
        self.wait_for_element(
            PageObjects.links_all.get("checkboxes"))
        self.click(
            PageObjects.links_all.get("checkboxes"))
        self.wait_for_element(
            PageObjects.checkBox_all.get("checkbox1"))
        self.click(PageObjects.checkBox_all.get("checkbox1"))
        web_elements = self.find_elements(
            PageObjects.checkBox_all.get("checkbox1"))
        self.assertTrue(web_elements[0].is_selected())
        self.go_back()
        self.page_readiness_wait()
        self.scroll_to_element(PageObjects.links_all.get('alerts'))
        self.click(PageObjects.links_all.get('alerts'))
        self.reload_page()
        self.click(PageObjects.buttons_all.get('js_alert'))
        self.switch_to_alert()
        sleep(5)
        self.wait_and_accept_alert()
        self.go_back()
        self.go_forward()
        self.click(PageObjects.buttons_all.get('js_confirm_alert'))
        self.switch_to_alert()
        sleep(5)
        self.wait_and_reject_alert()
        self.click(PageObjects.buttons_all.get('js_prompt_alert'))
        self.switch_to_alert()
        sleep(5)
        self.wait_and_reject_alert()
        self.go_back()
        self.click(PageObjects.links_all.get('frames'))
        self.click(PageObjects.links_all.get('iframe'))
        self.page_readiness_wait()
        self.switch_to_frame('mce_0_ifr')
        self.clear_text(PageObjects.text_boxes.get('text_in_frame'))
        self.switch_to_active_element()
        self.go_back()
        self.go_back()
        self.page_readiness_wait()
        sleep(5)
        self.click(PageObjects.links_all.get('dynamic_controls'))
        self.click(PageObjects.buttons_all.get('enable_btn'))
        sleep(5)
        self.send_keys(PageObjects.text_boxes.get('text_box'))
        sleep(5)
        self.switch_to_default_content()
        self.capture_screenshot(os.getcwd() + "\\example_Screenshot1.png")
        
    def test_multiple_tabs(self):
        self.open(PageObjects.base_url)
        self.set_window_size(1200, 800)
        width, height = self.get_current_window_size()
        self.assertTrue(width, 1200)
        self.assertTrue(height, 800)
        self.open_in_new_tab(PageObjects.bank_site_url)
        self.maximize()
        sleep(3)
        self.assertTrue((len(self.get_window_handles()), 2))
        self.close_current_window()

    def test_window_position(self):
        self.open(PageObjects.base_url)
        self.page_title_should_be(PageObjects.base_url_title)
        self.open_in_new_tab(PageObjects.bank_site_url)
        self.set_current_window_position(80, 40)
        x, y = self.get_current_window_size()
        self.assertTrue(x, 80)
        self.assertTrue(y, 40)
        sleep(3)
        self.close_all_windows()
