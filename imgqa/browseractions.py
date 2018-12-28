"""UI utility functions of all selenium self.driver based actions."""
from datetime import datetime

from time import sleep

import os

from selenium import webdriver

import logging

from selenium.common import exceptions as selenium_exceptions

from selenium.webdriver.support.ui import WebDriverWait as Wait

from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.select import Select

import unittest

import platform

from selenium.webdriver.common.by import By

from PIL import ImageGrab

WAIT_SLEEP_TIME = 0.1  # Seconds

TIME_OUT = 10  # Seconds


class BrowserActions(unittest.TestCase):
    """PageActions Class is the gateway for using Framework.

    It inherits Python's unittest.TestCase class, and runs with Pytest.
    """

    def __init__(self, *args, **kwargs):
        """Init Method for webdriver declarations."""
        super(BrowserActions, self).__init__(*args, **kwargs)
        self.by_value = None
        self.driver = webdriver.Chrome()

    # TBD: Decorator implementation
    # def page_readiness_wait(self, func):
    #     """Ensure page is awaited to be READY before any further action."""
    #     @functools.wraps(func)
    #     def page_ready(self, *args, **kargs):
    #         start = datetime.now()
    #         while (datetime.now() - start).total_seconds() < TIME_OUT:
    #             pagestate = self.driver.execute_script(
    #                 '''return document.readyState''')
    #             if pagestate.lower() == 'complete':
    #                 current_state = "Current page is in expected state {}"
    #                 logging.info(current_state.format(pagestate))
    #                 break
    #             sleep(0.2)
    #             if (datetime.now() - start).total_seconds() > TIME_OUT and
    #                pagestate.lower() != 'complete':
    #                 raise AssertionError(
    #                     "Opened browser is in state of %s" % pagestate)
    #         func(*args, **kargs)
    #     return page_ready

    def page_readiness_wait(self):
        """Web Page Expected to be in ready state."""
        start = datetime.now()
        while (datetime.now() - start).total_seconds() < TIME_OUT:
            pagestate = self.driver.execute_script(
                '''return document.readyState''')
            pagestate = pagestate.lower()
            if pagestate == 'complete':
                current_state = "Current page is in expected state {}"
                logging.info(current_state.format(pagestate))
                break
            sleep(0.2)
            loop_time_now = datetime.now() - start.total_seconds()
            if loop_time_now > TIME_OUT and pagestate != 'complete':
                raise AssertionError(
                    "Opened browser is in state of %s" % pagestate)

    # TBD: to be turned into decorator

    # def locator_check(self, func):
    #     """Local Method to classify the type of locator."""
    #     @functools.wraps(func)
    #     def consruct_locator(self, locator_dict):
    #         attributes = ('ID', 'NAME', 'LINK_TEXT', 'PARTIAL_LINK_TEXT',
    #                       'CLASS_NAME', 'XPATH', 'CSS_SELECTOR', 'TAG_NAME')
    #         if locator_dict['by'].upper() in attributes:
    #             self.by_value = "BY." + locator_dict['by'].upper()
    #         else:
    #             raise AssertionError("unknown %s" % locator_dict['by'])
    #         return self.func(locator_dict)
    #     return consruct_locator

    def locator_check(self, locator_dict):
        """Local Method to classify the type of locator."""
        text_retrived = locator_dict['by'].upper()
        if 'ID' in text_retrived:
            by = By.ID
        if 'CLASS_NAME' in text_retrived:
            by = By.CLASS_NAME
        if 'CSS_SELECTOR' in text_retrived:
            by = By.CSS_SELECTOR
        if 'NAME' in text_retrived:
            by = By.NAME
        if 'LINK_TEXT' in text_retrived:
            by = By.LINK_TEXT
        if 'PARTIAL_LINK_TEXT' in text_retrived:
            by = By.PARTIAL_LINK_TEXT
        if 'XPATH' in text_retrived:
            by = By.XPATH
        if 'TAG_NAME' in text_retrived:
            by = By.TAG_NAME
        self.by_value = by

    def open(self, url):
        """Open the passed 'url'."""
        if url is not None:
            try:
                self.driver.get(url)
                logging.info("Browser opened with url '{0}'".format(url))
            except Exception:
                logging.info("Browser with session id %s failed to navigate"
                             "to url '%s'." % (self.driver.session_id, url))
                raise AssertionError(
                    'Opened browser with session id {}'.format(
                        self.driver.session_id))
        else:
            raise AssertionError("Invalid/ URL cannot be null")

    def reload_page(self):
        """Method to refresh the page by selenium or java script."""
        try:
            self.driver.refresh()
        except BaseException:
            check_point1 = self.driver.execute_script(
                '''return performance.navigation.type''')
            self.driver.execute_script('''document.location.reload()''')
            check_point2 = self.driver.execute_script(
                '''return performance.navigation.type''')
            if check_point1 == 0 and check_point2 == 1:
                pass

    def get_page_source(self):
        """Return the entire HTML source of the current page or frame."""
        self.page_readiness_wait()
        return self.driver.page_source

    def get_title(self):
        """Return the title of current page."""
        self.page_readiness_wait()
        try:
            return self.driver.title
        except BaseException:
            return self.driver.execute_script("return document.title")

    def get_location(self):
        """Return the current browser URL using Selenium/Java Script."""
        self.page_readiness_wait()
        try:
            url = self.driver.current_url
        except BaseException:
            url = self.driver.execute_script("return window.location['href']")
        finally:
            return url if 'http' in url else None

    def get_attribute(self, locator, attribute_name=None):
        """Fetch attribute from provided locator.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param attribute_name: attribute name to get it's vale
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if not attribute_name and isinstance(locator, dict):
            return self.driver.find_element(
                self.by_value,
                value=locator['value']).get_attribute(attribute_name)
        else:
            raise AssertionError(
                "Invalid locator or Attribute is'{}'".format(attribute_name))

    def click(self, locator):
        """Click an element.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        """
        # self.locator_check(locator)
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            self.driver.find_element(self.by_value, value=locator['locatorvalue']).click()
        else:
            raise AssertionError("Locator type should be dictionary.")

    def send_keys(self, locator):
        """Send text but does not clear the existing text.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param string: string to send.
        """
        self.page_readiness_wait()
        if isinstance(locator, dict):
            self.locator_check(locator)
            elm = self.driver.find_element(self.by_value, locator['locatorvalue'])
            elm.send_keys(locator['value'])
            print('*********')
            print(elm)
            print(self.by_value)
            print(locator['value'])
            print('*********')

        else:
            raise AssertionError("Locator type should be dictionary.")

    def get_text(self, locator):
        """Get text from provided Locator.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            return self.driver.find_element(self.by_value,
                                            value=locator['value']).text
        else:
            raise AssertionError("Locator type should be dictionary.")

    def go_back(self):
        """Simulate back button on browser using selenium or js."""
        try:
            self.driver.back()
        except BaseException:
            self.driver.execute_script("window.history.go(-1)")

    def go_forward(self):
        """Simulate forward button on browser using  selenium or js."""
        try:
            self.driver.forward()
        except BaseException:
            self.driver.execute_script("window.history.go(+1)")

    def set_window_size(self, width, height):
        """Set width and height of the current window. (window.resizeTo).

        :param width: the width in pixels to set the window to
        :param height: the height in pixels to set the window to
        :Usage:
            driver.set_window_size(800,600).
        """
        width_value_check = isinstance(width, (int, float))
        height_value_check = isinstance(height, (int, float))
        if width_value_check and height_value_check:
            self.driver.set_window_size(width, height)
        else:
            AssertionError("Window size Invalid")

    def maximize(self):
        """Maximize the current window."""
        # https://bugs.chromium.org/p/chromedriver/issues/detail?id=985
        # reoccurs again and again
        if platform.system() == 'Darwin':
            img = ImageGrab.grab()
            screen_size = img.size
            self.set_window_size(screen_size[0], screen_size[1])
        else:
            self.driver.maximize_window()

    def get_driver_name(self):
        """Return the name of webdriver instance."""
        return self.driver.name

    def get_domain_url(self):
        """Method to extract domain url from webdriver itself."""
        url = self.get_current_url(self.driver)
        return url.split('//')[0] + '//' + url.split('/')[2]

    def clear_text(self, locator):
        """Clear the text if it's a text entry element.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            return self.driver.find_element(self.by_value,
                                            value=locator['value']).clear()
        else:
            raise AssertionError("Locator type should be dictionary")

    def capture_screenshot(self, filepath):
        """Save screenshot to the directory(existing or new one).

        :param filepath: file name with directory path(C:/images/image.png).
        """
        self.page_readiness_wait()
        if not self.drivers.current:
            self.info('Cannot capture screenshot because no browser is open.')
            return
        path = filepath.replace('/', os.sep)

        if not os.path.exists(path.split(os.sep)[0]):
            os.makedirs(path.split(os.sep)[0])
        elif os.path.exists(path):
            os.remove(path)
        if not self.driver.get_screenshot_as_file(path):
            raise RuntimeError("Failed to save screenshot '{}'.".format(path))
        return path

    def switch_to_active_element(self):
        """Return the element with focus, or BODY if nothing has focus."""
        self.page_readiness_wait()
        try:
            return self.driver.switch_to.active_element
        except BaseException:
            return self.driver.execute_script('''document.activeElement''')

    def switch_to_window(self, window):
        """Switch focus to the specified window using selenium/javascript.

        :param window: name of the window to switch
        """
        try:
            self.driver.switch_to.window(window)
        except selenium_exceptions.NoSuchWindowException:
            AssertionError(
                "Targeted window {} to be switched doesn't exist".window)

    def switch_to_frame(self, framename):
        """Switch focus to the specified frame using selenium/javascript.

        :param framename: name of the frame to switch.
        """
        self.page_readiness_wait()
        try:
            self.driver.switch_to.frame(framename)
        except selenium_exceptions.NoSuchFrameException:
            AssertionError(
                "Targeted frame {} to be switched doesn't exist".framename)

    def switch_to_default_content(self):
        """Switch focus to the default frame."""
        self.page_readiness_wait()
        try:
            self.driver.switch_to.default_content()
        except selenium_exceptions.InvalidSwitchToTargetException:
            AssertionError(
                "Frame or Window targeted to be switched doesn't exist")

    def switch_to_alert(self):
        """Switch focus to an alert on the page."""
        try:
            return self.driver.switch_to.alert
        except selenium_exceptions.NoAlertPresentException:
            AssertionError("Alert targeted to be switched doesn't exist")

    def hover_on_element(self, locator):
        """Hover on a particular element.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            try:
                ActionChains(self.driver).move_to_element(
                    self.driver.find_element(
                        self.by_value,
                        value=locator['value'])).perform()
            except selenium_exceptions.NoSuchElementException:
                AssertionError(
                    "Element{} not found".locator['by'] +
                    '=' + locator['value'])
        else:
            raise AssertionError("Locator type should be dictionary")

    def hover_on_click(self, locator):
        """Hover & click a particular element.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        try:
            self.hover_on_element(locator)
            self.click(locator)
        except selenium_exceptions.NoSuchElementException:
            AssertionError(
                "Element {} not found".locator['by'] + '=' + locator['value'])

    def wait_for_element(self, locator):
        """Wait for an element to exist in UI.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        try:
            if self.driver.find_element(self.by_value, value=locator['value']):
                return True
        except selenium_exceptions.NoSuchElementException:
            AssertionError("Failed to wait for element {}".format(
                locator['by'] + '=' + locator['value']))

    def wait_and_accept_alert(self):
        """Wait and accept alert present on the page."""
        try:
            Wait.until(ec.alert_is_present())
            self.driver.switch_to.alert.accept()
            logging.info("alert accepted")
        except selenium_exceptions.TimeoutException:
            logging.error(
                "Could Not Find Alert Within The Permissible Time Limit")

    def wait_and_reject_alert(self):
        """Wait for alert and rejects."""
        try:
            Wait.until(ec.alert_is_present())
            self.driver.switch_to.alert.dismiss()
            logging.info("alert dismissed")
        except selenium_exceptions.TimeoutException:
            logging.error(
                "Could Not Find Alert Within The Permissible Time Limit")

    def select_option_by_index(self, locator, index):
        """Select the option by index.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param index: integer value for index.
        """
        if isinstance(locator, dict) and isinstance(index, int):
            self.locator_check(locator)
            try:
                Select(self.driver.find_element(
                    self.by_value,
                    value=locator['value'])).select_by_index(index)
            except selenium_exceptions.NoSuchElementException:
                logging.error("Exception : Element '{}' Not Found".format(
                    locator['by'] + '=' + locator['value']))
        else:
            AssertionError(
                "Invalid locator '{}' or index '{}'".format(locator, index))

    def select_option_by_value(self, locator, value):
        """Select the option by using value.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param value: string value to select option.
        """
        self.page_readiness_wait()
        if isinstance(locator, dict) and isinstance(value, int):
            try:
                Select(self.driver.find_element(
                    self.by_value,
                    value=locator['value'])).select_by_value(value)
            except selenium_exceptions.NoSuchElementException:
                logging.error("Exception : Element '{}' Not Found".format(
                    locator['by'] + '=' + locator['value']))
        else:
            AssertionError(
                "Invalid locator '{}' or value '{}'".format(locator, value))

    def select_option_by_text(self, locator, text):
        """Select the value by using text.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param text: string value to select option.
        """
        self.page_readiness_wait()
        if isinstance(locator, dict):
            self.locator_check(locator)
            try:
                Select(self.driver.find_element(
                    self.by_value,
                    value=locator['value'])).select_by_visible_text(text)
            except selenium_exceptions.NoSuchElementException:
                logging.error("Exception : Element '{}' Not Found".format(
                    locator['by'] + '=' + locator['value']))
        else:
            AssertionError("Invalid locator type")

    def scroll_to_footer(self):
        """Scroll till end of the page."""
        self.page_readiness_wait()
        try:
            self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
        except selenium_exceptions.JavascriptException:
            logging.error('Exception : Not Able to Scroll To Footer')

    def scroll_to_element(self, locator):
        """Scroll to a particular element on the page.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        """
        self.page_readiness_wait()
        self.locator_check(locator)
        if isinstance(locator, dict):
            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true)",
                    self.driver.find_element(
                        self.by_value,
                        value=locator['value']))
            except selenium_exceptions.NoSuchElementException:
                logging.error('Exception : Not Able To Scroll to Element')
        else:
            AssertionError("Invalid locator type")

    def find_elements(self, locator):
        """Return elements matched with locator.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            return self.driver.find_elements(
                self.driver.find_element(
                    self.by_value,
                    value=locator['value']))
        else:
            AssertionError("Invalid locator type")
