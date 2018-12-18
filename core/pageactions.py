""" Common UI utility functions of all selenium self.driver based actions."""

from datetime import datetime

import Selenium2Library

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


class PageActions(unittest.TestCase):
    """
    PageActions Class is the gateway for using Framework.
    It inherits Python's unittest.TestCase class, and runs with Pytest.
    """

    def __init__(self, *args, **kwargs):
        super(PageActions, self).__init__(*args, **kwargs)

    # @pytest.fixture(autouse=True)
    # def classsetup(self):
        self.driver = webdriver.Chrome()

    def wait_for_page_ready_state(self):
        """
        Wait for Page to get back into ready state.
        TBD:Make this to be iterative based on settings.
        """
        try:
            sleep(1)
            output = self.driver.execute_script(
                '''return document.readyState''')
            if output == 'complete':
                return
            else:
                sleep(2)
                output1 = self.driver.execute_script(
                    '''return document.readyState''')
                if output1 == 'complete':
                    return
        except NoSuchElementException:
            pass

    def open(self, url=None):
        """Method helps to navigate to a specific url."""
        if url is not None:
            self.driver.get(url)
            self.wait_for_page_ready_state()

    def refresh_page(self):
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

    def get_page_source(self):
        """Page Source code extract in a string format."""
        src = self.driver.page_source
        if len(src) > 0:
            return src
        else:
            return "Unable to Fetch Page Source"

    def assert_page_title(self, titletocheck):
        """Evaluate Actual vs Expected Page Title."""
        try:
            title_src = self.driver.title
        except:
            title_src = self.driver.execute_script("return document.title")

        assert title_src == titletocheck

    def get_current_url(self):
        """Method Returns current url using Selenium/Java Script."""
        try:
            current_url = self.driver.current_url
        except:
            current_url = self.driver.execute_script(
                '''return window.location['href']''')
        finally:
            if 'http' in current_url:
                return self.driver.current_url
            else:
                return "Invalid HTTP URL"

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
        return by

    def elementcheck(self, locator_dict):
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
        return by

    def click(self, locator_dict):
        """Click an element."""
        self.wait_for_page_ready_state()
        self.driver.find_element(self.locator_check(
            locator_dict), value=locator_dict['locatorvalue']).click()

    def send_keys(self, locator_dict):
        """Send text but does not clear the existing text."""
        text_to_send = locator_dict['value']
        self.wait_for_page_ready_state()
        try:
            self.driver.find_element(
                self.locator_check(locator_dict), value=locator_dict['locatorvalue']).send_keys(text_to_send)
        except NoSuchElementException:
            pass

    def get_text(self, locator_dict):
        """Get text from provided Locator."""
        self.wait_for_page_ready_state()
        try:
            text = self.driver.find_element(
                self.locator_check(locator_dict), value=locator_dict['locatorvalue']).text
        except NoSuchElementException:
            pass
        return text

    def get_attribute(self, locator_dict):
        """Fetch attribute from provided locator."""
        attribute_to_get = locator_dict['value']
        self.wait_for_page_ready_state()
        try:
            attribute = self.driver.find_element(
                self.locator_check(locator_dict), value=locator_dict['locatorvalue']).get_attribute(attribute_to_get)
        except NoSuchElementException:
            pass
        return attribute

    def goback(self):
        """Perform a back button click either using selenium or javascript."""
        try:
            self.driver.back()
        except:
            self.driver.execute_script("window.history.go(-1)")
        finally:
            self.wait_for_page_ready_state()

    def goforward(self):
        """Perform a forward button click either using selenium or javascript."""
        try:
            self.driver.forward()
        except:
            self.driver.execute_script("window.history.go(+1)")
        finally:
            self.wait_for_page_ready_state()

    def set_window_size(self, width, height):
        """Resize self.driver Width and Height."""
        self.driver.set_window_size(width, height)

    def maximize(self):
        """Maximize self.driver window."""
        self.driver.maximize_window()

    def get_driver_name(self):
        """Return the Name(string) of self.driver on which tests are running."""
        return self.driver.name

    def get_domain_url(self):
        """Method to extract specific domain url from self.driver state itself."""
        url = self.get_current_url(self.driver)
        url_header = url.split('://')[0]
        simple_url = url.split('://')[1]
        base_url = simple_url.split('/')[0]
        domain_url = url_header + '://' + base_url
        return domain_url

    def clear_text(self, locator):
        """Clearing the existing text if present."""
        self.wait_for_page_ready_state()
        try:
            self.driver.find_element(
                self.locator_check(locator), locator['locatorvalue']).clear()
        except NoSuchElementException:
            pass

    def save_screenshot(self, name, folder=None):
        """Save screenshot to the directory(existing or new one)."""
        if folder:
            abs_path = os.path.abspath('.')
            file_path = abs_path + "/%s" % folder
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            screenshot_file = "%s/%s" % (file_path, name)
        else:
            screenshot_file = name
        self.driver.get_screenshot_as_file(screenshot_file)

    def wait_for_page_ready_state(self):
        """
        Wait for Page to get back into the ready state.
        Made this to be iterative based on settings.
        """
        try:
            maxtime = settings.LARGE_TIMEOUT
            for waittime in range(1, maxtime):
                sleep(waittime)
                output = self.driver.execute_script(
                    '''return document.readyState''')
                if output == 'complete':
                    return
        except:
            pass

    def switch_to_active_element(self):
        """Help to switch to active element in self.driver."""
        try:
            self.driver.switch_to.active_element
        except:
            self.driver.execute_script('''document.activeElement''')

    def switch_to_window(self, window):
        """Help to switch from window to window."""
        try:
            self.driver.switch_to.window(window)
        except selenium_exceptions.NoSuchWindowException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + \
                str(exc_tb.tb_lineno) + ' ' + 'Exception : Window Not Found'
            logging.error(message)

    def switch_to_frame(self, frame_name):
        """Help to switch from frame to frame."""
        try:
            self.driver.switch_to.frame(frame_name)
        except selenium_exceptions.NoSuchFrameException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + \
                str(exc_tb.tb_lineno) + ' ' + 'Exception : Frame Not Found'
            logging.error(message)

    def switch_to_default_content(self):
        """Help to switch to default content."""
        try:
            self.driver.switch_to_default_content()
        except selenium_exceptions.InvalidSwitchToTargetException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + str(exc_tb.tb_lineno) + \
                ' ' + 'Exception : Switch To Default Content Unsuccessful'
            logging.error(message)

    def switch_to_alert(self):
        """Help to switch to active alert on page."""
        try:
            alert = self.driver.switch_to.alert
            return alert
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + str(exc_tb.tb_lineno) + \
                ' ' + 'Exception : Alert Not Present In The Page'
            logging.error(message)

    def hover_on_element(self, locator_dict):
        """Help to hover on a particular element."""
        try:
            self.wait_for_page_ready_state()
            ActionChains(self.driver).move_to_element(self.driver.find_element(
                self.locator_check(locator_dict), value=locator_dict['locatorvalue'])).perform()
        except selenium_exceptions.NoSuchElementException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + \
                str(exc_tb.tb_lineno) + ' ' + 'Exception : Element Not Found'
            logging.error(message)

    def hover_on_click(self, locator_dict):
        """Help to hover & click a particular element."""
        try:
            self.hover_on_element(self.driver, locator_dict)
            self.click(self.driver, locator_dict)
        except selenium_exceptions.NoSuchElementException as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + \
                str(exc_tb.tb_lineno) + ' ' + 'Exception : Element Not Found'
            logging.error(message)

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

    def wait_for_element(self, locator_dict):
        """Halt for an element upon page."""
        try:
            WebDriverWait(self.driver, settings.EXTREME_TIMEOUT).until(
                ec.presence_of_element_located((self.locator_check(locator_dict), locator_dict['locatorvalue'])))
        except selenium_exceptions.TimeoutException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + str(exc_tb.tb_lineno) + ' ' + \
                'Timeout Exception : Element Fialed TO Load Within The Permissible Time Limit'
            logging.error(message)

    def wait_for_and_accept_alert(self):
        """Help accept an alert present on the page."""
        try:
            wait = WebDriverWait(self, settings.EXTREME_TIMEOUT)
            wait.until(ec.alert_is_present())
            self.driver.switch_to.alert.accept()
            print("alert accepted")
        except selenium_exceptions.TimeoutException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + str(exc_tb.tb_lineno) + ' ' + \
                'Timeout Exception : Could Not Find Alert Within The Permissible Time Limit'
            logging.error(message)

    def wait_for_and_reject_alert(self):
        """Help to accept an alert present on the page."""
        try:
            wait = WebDriverWait(self.driver, settings.EXTREME_TIMEOUT)
            wait.until(ec.alert_is_present())
            self.driver.switch_to.alert.dismiss()
            print("alert dismissed")
        except selenium_exceptions.TimeoutException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + str(exc_tb.tb_lineno) + ' ' + \
                'Timeout Exception : Could Not Find Alert Within The Permissible Time Limit'
            logging.error(message)

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

    def pick_select_option_by_index(self, locator_dict, n):
        """Select the value by using index."""
        try:
            Select(self.driver.find_element(self.locator_check(
                locator_dict), value=locator_dict['locatorvalue'])).select_by_index(n)
        except selenium_exceptions.NoSuchElementException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + \
                str(exc_tb.tb_lineno) + ' ' + 'Exception : Element Not Found'
            logging.error(message)

    def pick_select_option_by_value(self, locator_dict, value):
        """Select the value by using value."""
        try:
            Select(self.driver.find_element(self.locator_check(locator_dict),
                                             value=locator_dict['locatorvalue'])).select_by_value(value)
        except selenium_exceptions.NoSuchElementException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + \
                str(exc_tb.tb_lineno) + ' ' + 'Exception : Element Not Found'
            logging.error(message)

    def pick_select_option_by_text(self, locator_dict, text):
        """Select the value by using text."""
        try:
            Select(self.driver.find_element(self.locator_check(locator_dict),
                                             value=locator_dict['locatorvalue'])).select_by_visible_text(text)
        except selenium_exceptions.NoSuchElementException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + \
                str(exc_tb.tb_lineno) + ' ' + 'Exception : Element Not Found'
            logging.error(message)

    def scroll_to_footer(self):
        """Scroll till end of the page."""
        try:
            self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
        except selenium_exceptions.JavascriptException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + str(exc_tb.tb_lineno) + \
                ' ' + 'Exception : Not Able to Scroll To Footer'
            logging.error(message)

    def scroll_to_element(self, locator_dict):
        """Scroll to a particular element on the page. Invalid method yet."""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true)", self.driver.find_element(
                self.locator_check(locator_dict), value=locator_dict['locatorvalue']))
        except selenium_exceptions.NoSuchElementException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = str(exc_type) + ' ' + fname + ' ' + str(exc_tb.tb_lineno) + \
                ' ' + 'Exception : Not Able To Scroll to Element'
            logging.error(message)

    # TODO
    def double_click(self, locator_dict):
        """TODO: Works in firefox but not in chrome Double click on any element."""
        self.driver.click(self.driver, locator_dict)
        sleep(0.2)
        self.driver.click(self.driver, locator_dict)
        # review yet to do

    def is_xpath_selector(self, locator_dict):
        """Determine selector is an xpath."""
        if (locator_dict['locatorvalue'].startswith('/') or
                locator_dict['locatorvalue'].startswith('./') or
                locator_dict['locatorvalue'].startswith('(')):
            return True
        return False

    def is_link_text_selector(self, locator_dict):
        """Determine if a selector is a link text selector."""
        if (locator_dict['locatorvalue'].startswith('link=') or
                locator_dict['locatorvalue'].startswith('link_text=')):
            return True
        return False

    def get_link_text_from_selector(self, locator_dict):
        """Get the link text from a link text selector."""
        if locator_dict['locatorvalue'].startswith('link='):
            return locator_dict['locatorvalue'].split('link=')[1]
        elif locator_dict['locatorvalue'].startswith('link_text='):
            return locator_dict['locatorvalue'].split('link_text=')[1]
        return locator_dict

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

    def find_elements(self, locator_dict):
        """Method to find elements - needed parent locator as input parameter."""
        return self.driver.find_elements(self.locator_check(locator_dict), value=locator_dict['locatorvalue'])
