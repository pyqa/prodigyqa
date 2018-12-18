""" Common UI utility functions of all selenium self.driver based actions."""
import Selenium2Library

from datetime import datetime

from time import sleep

import functools

import sys

import os

import csv

from selenium import webdriver

import time

import logging

from imgqa.objectrepo import settings

from time import sleep

from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions as selenium_exceptions

from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By

from selenium.webdriver.support.select import Select
try:
    # Selenium 3 (ElementNotInteractableException does not exist in selenium 2)
    ENI_Exception = selenium_exceptions.ElementNotInteractableException
except Exception:
    # Selenium 2 (Keep compatibility with seleneium 2.53.6 if still being used)
    ENI_Exception = selenium_exceptions.ElementNotSelectableException

import unittest

WAIT_SLEEP_TIME = 0.1

TIME_OUT = 10


class PageActions(unittest.TestCase):
    """
    PageActions Class is the gateway for using Framework.
    It inherits Python's unittest.TestCase class, and runs with Pytest.
    """

    def __init__(self, browser_name="chrome", *args, **kwargs):
        super(PageActions, self).__init__(*args, **kwargs)
        if browser_name.lower() == "chrome":
            self.driver = webdriver.Chrome()
        elif browser_name.lower() == "firefox":
            self.driver = webdriver.Firefox()

    def page_readiness_wait(func):
        """ wait for page ready state
            Description: Wait for page to ready state.
        """
        @functools.wraps(func)
        def wait_for_page_ready_state(self, *args, **kargs):
            start = datetime.now()
            while (datetime.now() - start).total_seconds() < TIME_OUT:
                pagestate = self.driver.execute_script('''return document.readyState''')
                if pagestate.lower() == 'complete':
                    logging.info("Current page is in excpected state %s" %pagestate)
                    break
                sleep(0.2)
                if (datetime.now() - start).total_seconds() > TIME_OUT and pagestate.lower() != 'complete':
                    raise AssertionError("Opened browser is in state of %s" %pagestate)
            func(*args, **kargs)
        return wait_for_page_ready_state

    def open(self, url=None):
        """Opens a new browser instance to the given 'url'."""
        if url is not None:
            try:
                self.driver.get(url)
                logging.info("Browser opened with url '%s' and page title is '%s'" % (url, self.driver.title()))
            except Exception:
                self.debug("Opened browser with session id %s but failed "
                           "to open url '%s'." % (self.driver.session_id, url))
                raise
            self.debug('Opened browser with session id %s.' % self.driver.session_id)
        else:
            raise AssertionError("url should not be null")

    @page_readiness_wait
    def reload_page(self):
        """Method to refresh the page by selenium or java script."""
        try:
            self.driver.refresh()
        except:
            check_point1 = self.driver.execute_script(
                '''return performance.navigation.type''')
            self.driver.execute_script('''document.location.reload()''')
            check_point2 = self.driver.execute_script(
                '''return performance.navigation.type''')
            if check_point1 == 0 and check_point2 == 1:
                pass

    @page_readiness_wait
    def get_page_source(self):
        """Returns the entire HTML source of the current page or frame."""
        return self.driver.page_source

    @page_readiness_wait
    def get_title(self):
        """Returns the title of current page."""
        try:
            return self.driver.title
        except:
            return self.driver.execute_script("return document.title")

    # RO
    def assert_page_title(self, titletocheck):
        """Evaluate Actual vs Expected Page Title."""
        try:
            title_src = self.driver.title
        except:
            title_src = self.driver.execute_script("return document.title")

        assert title_src == titletocheck

    @page_readiness_wait
    def get_location(self):
        """Returns the current browser URL using Selenium/Java Script."""
        try:
            url = self.driver.current_url
        except:
            url = self.driver.execute_script("return window.location['href']")
        finally:
            return url if 'http' in url else None

    def locator_check(self, locator):
        """Local Method to classify the type of locator.
        :param locator: locator name and value
            example: ID.start-of-content"""
        locators = ["ID", "NAME", "LINK_TEXT", "PARTIAL_LINK_TEXT", "CLASS_NAME", "XPATH", "CSS_SELECTOR", "TAG_NAME"]
        if locator.upper() in locators:
            return "BY." + locator.upper()
        else:
            raise AssertionError("unknown %s" % locator)

    # RO
    @page_readiness_wait
    def click(self, locator):
        """Click an element.
        :param locator: locator name and value
            example: ID.start-of-content"""
        self.driver.find_element(self.locator_check(
            locator.split('.')[0]), value=locator.split('.')[1]).click()

    @page_readiness_wait
    def send_keys(self, locator, string):
        """Send text but does not clear the existing text.
        :parm locator: locator name and value
            example: ID.start-of-content
        :parm string: string to send"""
        self.driver.find_element(self.locator_check(
            locator.split('.')[0]), value=locator.split('.')[1]).send_keys(string)

    @page_readiness_wait
    def get_text(self, locator):
        """Get text from provided Locator.
        :param locator: locator name and value
            example: ID.start-of-content."""
        return self.driver.find_element(self.locator_check(
            locator.split('.')[0]), value=locator.split('.')[1]).text

    @page_readiness_wait
    def get_attribute(self, locator, attribute_name):
        """Fetch attribute from provided locator.
        :param locator: locator name and value
            example: ID.start-of-content.
        :param attribute_name: attribute name to get it's vale"""
        return self.driver.find_element(self.locator_check(
            locator.split('.')[0]), value=locator.split('.')[1]).get_attribute(attribute_name)

    @page_readiness_wait
    def go_back(self):
        """Simulates the user clicking the back button on their browser using either selenium or javascript."""
        try:
            self.driver.back()
        except:
            self.driver.execute_script("window.history.go(-1)")

    @page_readiness_wait
    def go_forward(self):
        """Simulates the user clicking the forward button on their browser using either selenium or javascript."""
        try:
            self.driver.forward()
        except:
            self.driver.execute_script("window.history.go(+1)")

    @page_readiness_wait
    def set_window_size(self, width, height):
        """Sets the width and height of the current window. (window.resizeTo)
        :param width: the width in pixels to set the window to
        :param height: the height in pixels to set the window to

        :Usage:
            driver.set_window_size(800,600)."""
        self.driver.set_window_size(width, height)

    @page_readiness_wait
    def maximize(self):
        """Maximizes the current window that webdriver is using"""
        self.driver.maximize_window()

    @page_readiness_wait
    def get_driver_name(self):
        """Returns the name of the underlying browser for this instance."""
        return self.driver.name

    @page_readiness_wait
    def get_domain_url(self):
        """Method to extract specific domain url from self.driver state itself."""
        url = self.get_current_url(self.driver)
        return url.split('//')[0] + '//' + url.split('/')[2]

    @page_readiness_wait
    def clear_text(self, locator):
        """Clears the text if it's a text entry element."""
        self.driver.find_element(self.locator_check(
            locator.split('.')[0]), value=locator.split('.')[1]).clear()

    @page_readiness_wait
    def capture_screenshot(self, filepath):
        """Save screenshot to the directory(existing or new one).
        :param filepath: file name with directory path
            Ex: C:/images/image.png"""
        if not self.drivers.current:
            self.info('Cannot capture screenshot because no browser is open.')
            return
        path = filepath.replace('/', os.sep)

        if not os.path.exists(path.split(os.sep)[0]):
            os.mkdir(path.split(os.sep)[0])
        elif os.path.exists(path):
            os.remove(path)
        if not self.driver.get_screenshot_as_file(path):
            raise RuntimeError("Failed to save screenshot '{}'.".format(path))

    @page_readiness_wait
    def switch_to_active_element(self):
        """Returns the element with focus, or BODY if nothing has focus."""
        try:
            return self.driver.switch_to.active_element
        except:
            return self.driver.execute_script('''document.activeElement''')

    @page_readiness_wait
    def switch_to_window(self, window):
        """Switches focus to the specified window using selenium/javascript.
        :param window: name of the window to switch"""
        try:
            self.driver.switch_to.window(window)
        except selenium_exceptions.NoSuchWindowException:
            pass

    @page_readiness_wait
    def switch_to_frame(self, framename):
        """Switches focus to the specified frame using selenium/javascript.
        :param framename: name of the frame to switch"""
        try:
            self.driver.switch_to.frame(framename)
        except selenium_exceptions.NoSuchFrameException:
            pass

    @page_readiness_wait
    def switch_to_default_content(self):
        """Switch focus to the default frame."""
        try:
            self.driver.switch_to.default_content()
        except selenium_exceptions.InvalidSwitchToTargetException:
            pass

    @page_readiness_wait
    def switch_to_alert(self):
        """Switches focus to an alert on the page."""
        try:
            return self.driver.switch_to.alert
        except selenium_exceptions.NoAlertPresentException:
            pass

    @page_readiness_wait
    def hover_on_element(self, locator):
        """Hover on a particular element.
        :param locator: locator name and value
            example: ID.start-of-content"""
        try:
            ActionChains(self.driver).move_to_element(self.driver.find_element(self.locator_check(
                locator.split('.')[0]), value=locator.split('.')[1])).perform()
        except selenium_exceptions.NoSuchElementException:
            pass

    @page_readiness_wait
    def hover_on_click(self, locator):
        """Hover & click a particular element.
        :param locator: locator name and value
            example: ID.start-of-content"""
        try:
            self.hover_on_element(locator)
            self.click(locator)
        except selenium_exceptions.NoSuchElementException:
            pass

    # PO
    def element_assert(self, locator_dict):
        """Help to verify the element."""
        try:
            self.driver.find_element(self.locator_check(
                locator_dict), value=locator_dict['locatorvalue'])
        except selenium_exceptions.NoSuchElementException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + \
                str(exc_tb.tb_lineno) + ' ' + 'Exception : Element Not Found'
            logging.error(message)
            return False
        return True

    @page_readiness_wait
    def wait_for_element(self, locator):
        """Waits for an element to exist in UI."""
        try:
            if self.driver.find_element(self.locator_check(locator.split('.')[0]), value=locator.split('.')[1]):
                return True
        except selenium_exceptions.NoSuchElementException:
            AssertionError("Failed to wait for element '%s'" % locator.split('.')[1])

    @page_readiness_wait
    def wait_and_accept_alert(self):
        """Waits and accepts alert present on the page."""
        try:
            wait = WebDriverWait(self, settings.EXTREME_TIMEOUT)
            wait.until(ec.alert_is_present())
            self.driver.switch_to.alert.accept()
            logging.info("alert accepted")
        except selenium_exceptions.TimeoutException:
            logging.error("Could Not Find Alert Within The Permissible Time Limit")

    @page_readiness_wait
    def wait_and_reject_alert(self):
        """Waits for alert and rejects."""
        try:
            wait = WebDriverWait(self.driver, settings.EXTREME_TIMEOUT)
            wait.until(ec.alert_is_present())
            self.driver.switch_to.alert.dismiss()
            logging.info("alert dismissed")
        except selenium_exceptions.TimeoutException:
            logging.error("Could Not Find Alert Within The Permissible Time Limit")

    # TODO
    def page_performance_capture(self, url):
        """Capture important metrics out into a datafile."""
        nav_start = self.driver.execute_script(
            """return performance.timing.navigationStart""")
        res_start = self.driver.execute_script(
            """return performance.timing.responseStart""")
        self.open_self.driver(self.driver, url)
        dom_complete = self.driver.execute_script(
            """return performance.timing.domComplete""")
        # Converting milliseconds to seconds
        navigationstart = nav_start / 1000
        responsestart = res_start / 1000
        domcomplete = dom_complete / 1000
        # calculating Backend time to load page
        backend_time = responsestart - navigationstart
        # calculating Frontend time to load page
        frontend_time = domcomplete - responsestart
        # Converting milliseconds to timestamp and string format
        navigation_started = str(datetime.datetime.fromtimestamp(
            navigationstart).strftime('%Y-%m-%d %H:%M:%S'))
        response_started = str(datetime.datetime.fromtimestamp(
            responsestart).strftime('%Y-%m-%d %H:%M:%S'))
        domcompleted = str(datetime.datetime.fromtimestamp(
            domcomplete).strftime('%Y-%m-%d %H:%M:%S'))
        fields = [url, navigation_started, response_started,
                  domcompleted, backend_time, frontend_time]
        with open('performance.csv', 'ab') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    @page_readiness_wait
    def select_option_by_index(self, locator, index):
        """Select the option by index.
        :param locator: locator name and value
            example: ID.start-of-content
        :param index: integer value for index."""
        try:
            Select(self.driver.find_element(self.locator_check(locator.split('.')[0]),
                                            value=locator.split('.')[1])).select_by_index(index)
        except selenium_exceptions.NoSuchElementException:
            logging.error('Exception : Element Not Found')

    @page_readiness_wait
    def select_option_by_value(self, locator, value):
        """Select the option by using value.
        :param locator: locator name and value
            example: ID.start-of-content
        :param value: string value to select option."""
        try:
            Select(self.driver.find_element(self.locator_check(locator.split('.')[0]),
                                            value=locator.split('.')[1])).select_by_value(value)
        except selenium_exceptions.NoSuchElementException:
            logging.error('Exception : Element Not Found')

    @page_readiness_wait
    def select_option_by_text(self, locator, text):
        """Select the value by using text.
        :param locator: locator name and value
            example: ID.start-of-content
        :param value: string value to select option."""
        try:
            Select(self.driver.find_element(self.locator_check(locator.split('.')[0]),
                                            value=locator.split('.')[1])).select_by_visible_text(text)
        except selenium_exceptions.NoSuchElementException:
            logging.error('Exception : Element Not Found')

    @page_readiness_wait
    def scroll_to_footer(self):
        """Scroll till end of the page."""
        try:
            self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
        except selenium_exceptions.JavascriptException:
            logging.error('Exception : Not Able to Scroll To Footer')

    @page_readiness_wait
    def scroll_to_element(self, locator):
        """Scroll to a particular element on the page.
        :param locator: locator name and value
            example: ID.start-of-content"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true)",
                                       self.driver.find_element(self.locator_check(locator.split('.')[0]),
                                                                value=locator.split('.')[1]))
        except selenium_exceptions.NoSuchElementException:
            logging.error('Exception : Not Able To Scroll to Element')

    # TODO
    def double_click(self, locator_dict):
        """TODO: Works in firefox but not in chrome Double click on any element."""
        self.driver.click(self.driver, locator_dict)
        sleep(0.2)
        self.driver.click(self.driver, locator_dict)
        # review yet to do

    # PO
    def is_xpath_selector(self, locator_dict):
        """Determine selector is an xpath."""
        if (locator_dict['locatorvalue'].startswith('/') or
                locator_dict['locatorvalue'].startswith('./') or
                locator_dict['locatorvalue'].startswith('(')):
            return True
        return False

    # PO
    def is_link_text_selector(self, locator_dict):
        """Determine if a selector is a link text selector."""
        if (locator_dict['locatorvalue'].startswith('link=') or
                locator_dict['locatorvalue'].startswith('link_text=')):
            return True
        return False

    # PO
    def get_link_text_from_selector(self, locator_dict):
        """Get the link text from a link text selector."""
        if locator_dict['locatorvalue'].startswith('link='):
            return locator_dict['locatorvalue'].split('link=')[1]
        elif locator_dict['locatorvalue'].startswith('link_text='):
            return locator_dict['locatorvalue'].split('link_text=')[1]
        return locator_dict

    # PO
    def wait_for_element_visible(self, locator_dict, timeout=settings.LARGE_TIMEOUT):
        """
        Search for the specified element by the given selector.
        Returns the element object if the element is present and visible on page.
        Raises an exception if the element does not appear within timeout.
        @Params
        driver - the webdriver object (required)
        selector - the locator that is used (required)
        by - the method to search for the locator (Default: By.CSS_SELECTOR)
        timeout - the time to wait for elements in seconds
        @Returns
        A web element object.
        """
        element = None
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout * 10)):
            try:
                element = self.driver.find_element(self.locator_check(
                    locator_dict), value=locator_dict['locatorvalue'])
                if element.is_displayed():
                    return element
                else:
                    element = None
                    raise Exception()
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        if not element and self.locator_check(
                locator_dict) != By.LINK_TEXT:
            raise selenium_exceptions.ElementNotVisibleException(
                "Element {%s} was not visible after %s second%s!" % (
                    locator_dict['locatorvalue'], timeout, plural))
        if not element and self.locator_check(
                locator_dict) == By.LINK_TEXT:
            raise selenium_exceptions.ElementNotVisibleException(
                "Link text {%s} was not visible after %s second%s!" % (
                    locator_dict['locatorvalue'], timeout, plural))

    # PO
    def wait_for_element_present(self, locator_dict, timeout=settings.LARGE_TIMEOUT):
        """
        Search for the specified element by the given selector. Returns the
        element object if the element is present on the page. The element can be
        invisible. Raises an exception if the element does not appear in the
        specified timeout.
        @Params
        driver - the webdriver object
        selector - the locator that is used (required)
        by - the method to search for the locator (Default: By.CSS_SELECTOR)
        timeout - the time to wait for elements in seconds
        @Returns
        A web element object
        """

        element = None
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout * 10)):
            try:
                element = self.driver.find_element(self.locator_check(
                    locator_dict), value=locator_dict['locatorvalue'])
                return element
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                sleep(0.1)
        if not element:
            raise NoSuchElementException(
                "Element {%s} was not present after %s seconds!" % (
                    locator_dict['locatorvalue'], timeout))

    # PO
    def is_element_visible(self, locator_dict):
        """Check if the element is actually visible."""
        if self.is_xpath_selector(self.locator_check(
                locator_dict)):
            by = By.XPATH
        if self.is_link_text_selector(self.locator_check(
                locator_dict)):
            locator_dict['locatorvalue'] = self.get_link_text_from_selector(self.locator_check(
                locator_dict))
            locator_dict['by'] = By.LINK_TEXT
        return self.is_element_visible(self.driver, locator_dict)

    # PO
    def highlight(self, locator_dict):
        """Highlight (blinks) a Selenium Webdriver element."""
        driver = self.driver.find_element(
            self.locator_check(locator_dict), value=locator_dict['locatorvalue'])._parent

        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                  self.driver.find_element(
                                      self.locator_check(locator_dict),
                                      value=locator_dict['locatorvalue']), s)
        original_style = self.driver.find_element(
            self.locator_check(locator_dict),
            value=locator_dict['locatorvalue']).get_attribute('style')
        apply_style("background: green; border: 2px solid red;")
        time.sleep(.4)
        apply_style(original_style)

    @page_readiness_wait
    def find_elements(self, locator):
        """Returns elements matched with locator.
        :param locator: locator name and value
            example: ID.start-of-content"""
        return self.driver.find_elements(self.driver.find_element(self.locator_check(locator.split('.')[0]),
                                                                value=locator.split('.')[1]))
