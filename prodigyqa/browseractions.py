"""UI utility functions of all selenium self.driver based actions."""
from loguru import logger

import os

import platform

import unittest

from datetime import datetime

from time import sleep

from selenium.common import exceptions as selenium_exceptions

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.support.select import Select

from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.ui import WebDriverWait as Wait

from selenium import webdriver
from seleniumwire import webdriver as wire_webdriver

if platform.system() == 'Darwin':
    from PIL import ImageGrab

WAIT_SLEEP_TIME = 0.1  # Seconds

TIME_OUT = 10  # Seconds

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True


class BrowserActions(unittest.TestCase):
    """PageActions Class is the gateway for using Framework.

    It inherits Python's unittest.TestCase class, and runs with Pytest.
    """

    def __init__(self, *args, **kwargs):
        """Init Method for webdriver declarations.

                To invoke chrome/firefox browser pass corresponding values,
                bydefault chrome will be invoked.
                To access browser network calls 'intercept' with True value
                needs to
                passed in kwargs.
                To achieve this we are using selenium wire
                https://pypi.org/project/selenium-wire/
        :param args pass the required data as list
        :param kwargs: pass the required data as dict
        """

        browser = kwargs.pop('browser', None)
        intercept = kwargs.pop('intercept', None)
        super(BrowserActions, self).__init__(*args, **kwargs)
        self.by_value = None
        driver_obj = wire_webdriver if intercept else webdriver
        headless_exec = True if platform.system() == 'Linux' else False


        if browser == 'firefox':
            self.driver = driver_obj.Firefox(
                firefox_options=firefox_options if headless_exec else None)
        # running scripts with firefox browser
        else:
            self.driver = driver_obj.Chrome(
                chrome_options=chrome_options if headless_exec else None)

    def __del__(self):
        """Destructor method to kill the driver instance.
        This helps to kill the driver instance at the end of the execution.
        """
        self.driver.quit()

    def page_readiness_wait(self):
        """Web Page Expected to be in ready state."""
        start = datetime.now()
        while (datetime.now() - start).total_seconds() < TIME_OUT:
            pagestate = self.__execute_script('''return document.readyState''')
            pagestate = pagestate.lower()
            if pagestate == 'complete':
                current_state = "Current page is in expected state {}"
                logger.info(current_state.format(pagestate))
                break
            sleep(0.2)
            loop_time_now = datetime.now() - start.total_seconds()
            if loop_time_now > TIME_OUT and pagestate != 'complete':
                raise AssertionError(
                    "Opened browser is in state of %s" % pagestate)

    def locator_check(self, locator_dict):
        """Local Method to classify locator type.

        :type locator_dict: dict
        """
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
                logger.info("Browser opened with url '{0}'".format(url))
            except Exception:
                logger.info("Browser with session id %s failed"
                            " to navigate to url '%s'." % (
                                self.driver.session_id, url))
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
            check_point1 = self.__execute_script(
                '''return performance.navigation.type''')
            self.__execute_script('''document.location.reload()''')
            check_point2 = self.__execute_script(
                '''return performance.navigation.type''')
            if check_point1 == 0 and check_point2 == 1:
                logger.info("Page Refresh Complete")
            else:
                logger.error("Page Refresh Error")

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
            return self.__execute_script("return document.title")

    def get_location(self):
        """Return the current browser URL using Selenium/Java Script."""
        self.page_readiness_wait()
        try:
            url = self.driver.current_url
        except BaseException:
            url = self.__execute_script("return window.location['href']")
        finally:
            return url if 'http' in url else None

    def get_attribute(self, locator=None, element=None,
                      attribute_name=None, type='locator'):
        """Fetch attribute from locator/element/parent.

        element with child locator.
        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param attribute_name: attribute name to get it's vale
        :param element: it is a webelement
        :param type : value can only be 'locator' or 'element' or 'mixed'
        :type locator: dict
        :type type: str
        """
        valid_arguments_of_type = ['locator', 'element', 'mixed']
        type = type.lower()
        if type not in valid_arguments_of_type:
            raise AssertionError("Invalid Type Specified")
        if locator is None and element is None and attribute_name is None:
            raise AssertionError("Invalid Specification/condition")
        if type == 'locator':
            if locator is not None and attribute_name is not None:
                self.locator_check(locator)
                self.page_readiness_wait()
                if attribute_name is not None and isinstance(locator, dict):
                    return self.driver.find_element(
                        self.by_value,
                        value=locator['locatorvalue']).get_attribute(
                            attribute_name)
                else:
                    raise AssertionError(
                        "Invalid locator or Attribute is'{}'".format(
                            attribute_name))

        if type == 'element':
            if element is not None and attribute_name is not None:
                self.page_readiness_wait()
                return element.get_attribute(attribute_name)
            else:
                raise AssertionError(
                    "Invalid Element/Attribute passed:'{}'".format(
                        attribute_name))
        if type == 'mixed':
            if element is not None:
                if locator is not None and attribute_name is not None:
                    self.locator_check(locator)
                    self.page_readiness_wait()
                    if isinstance(locator, dict):
                        return element.find_element(
                            self.by_value,
                            value=locator['locatorvalue']).get_attribute(
                                attribute_name)
                    else:
                        raise AssertionError(
                            "Invalid locator/element/attribute'{}'".format(
                                attribute_name))

    def click(self, locator, index=None):
        """Click an element.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param index: Defaults None, number/position of element
        """
        self.page_readiness_wait()
        if isinstance(locator, dict):
            self.locator_check(locator)
            if index is not None:
                web_elts = self.find_elements(locator)
                if index < len(web_elts):
                    web_elts[index].click()
                else:
                    raise AssertionError(
                        "Index is greater than no. of elements present")
            else:
                self.__find_element(locator).click()
        elif isinstance(locator, WebElement):
            locator.click()
        else:
            raise AssertionError(
                "Dictionary/Weblement are valid Locator types.")

    def javascript_click(self, locator, index=None):
        """Javascript Click on provided element.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'})
            or a Webelement.
        :param index: Number/position of element present
        """
        self.page_readiness_wait()
        if isinstance(locator, dict):
            self.locator_check(locator)
            if index is not None:
                web_elts = self.find_elements(locator)
                if index < len(web_elts):
                    self.driver.execute_script(
                        "arguments[0].click();", web_elts[index])
                else:
                    raise AssertionError(
                        "Index is greater than the number of elements")
            else:
                self.driver.execute_script(
                    "arguments[0].click();", self.driver.find_element(
                        self.by_value, value=locator['locatorvalue']))
        elif isinstance(locator, WebElement):
            self.__execute_script("arguments[0].click();", locator)
        else:
            raise AssertionError(
                "Locator type should be either dictionary or Weblement.")

    def is_element_displayed(self, locator: dict):
        """
        Check whether an element is diplayed.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :type locator: dict
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            return self.driver.find_element(
                self.by_value,
                value=locator['locatorvalue']).is_displayed()
        else:
            raise AssertionError("Locator type should be dictionary.")

    def is_element_enabled(self, locator: dict):
        """
        Check whether an element is enabled.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :type locator: dict
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            return self.__find_element(locator).is_enabled()
        else:
            raise AssertionError("Locator type should be dictionary.")

    def is_element_selected(self, locator: dict):
        """
        Check whether an element is selecte.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :type locator: dict
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            return self.__find_element(locator).is_selected()
        else:
            raise AssertionError("Locator type should be dictionary.")

    def send_keys(self, locator: dict, value=None):
        """Send text but does not clear the existing text.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :type locator: dict
        """
        self.page_readiness_wait()
        if isinstance(locator, dict):
            self.locator_check(locator)

            self.__find_element(locator).send_keys(
                locator['value'] if value is None else value)
        else:
            raise AssertionError("Locator type should be dictionary.")

    def get_text(self, locator, index=None):
        """Get text from provided Locator.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        """
        self.page_readiness_wait()
        if isinstance(locator, dict):
            self.locator_check(locator)
            if index is not None:
                web_elts = self.find_elements(locator)
                if index < len(web_elts):
                    return web_elts[index].text
                else:
                    raise AssertionError(
                        "Index is greater than the number of elements")
            else:
                return self.__find_element(locator).text

        elif isinstance(locator, WebElement):
            return locator.text
        else:
            raise AssertionError(
                "Locator type should be either dictionary or Weblement.")

    def go_back(self):
        """Simulate back button on browser using selenium or js."""
        try:
            self.driver.back()
        except BaseException:
            self.__execute_script("window.history.go(-1)")

    def go_forward(self):
        """Simulate forward button on browser using  selenium or js."""
        try:
            self.driver.forward()
        except BaseException:
            self.__execute_script("window.history.go(+1)")

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
        url = self.driver.current_url
        return url.split('//')[0] + '//' + url.split('/')[2]

    def clear_text(self, locator: dict):
        """Clear the text if it's a text entry element.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :type locator: dict
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            return self.__find_element(locator).clear()
        else:
            raise AssertionError("Locator type should be dictionary")

    def capture_screenshot(self, filepath):
        """Save screenshot to the directory(existing or new one).

        :param filepath: file name with directory path(C:/images/image.png).
        """
        self.page_readiness_wait()

        if not self.driver.service.process:
            logger.info('Cannot capture ScreenShot'
                        ' because no browser is open.')
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
            return self.__execute_script('''document.activeElement''')

    def switch_to_window(self, window):
        """Switch focus to the specified window using selenium/javascript.

        :param window: name of the window to switch
        """
        try:
            self.driver.switch_to.window(window)
        except selenium_exceptions.NoSuchWindowException:
            AssertionError(
                "Targeted window {} to be switched doesn't exist".window)

    def switch_to_active_window(self):
        """Switch focus to Active window."""
        try:
            handles = self.driver.window_handles
            size = len(handles)
            for x in range(size):
                if handles[x] != self.driver.current_window_handle:
                    self.driver.switch_to.window(handles[x])
        except selenium_exceptions.NoSuchWindowException:
            AssertionError(
                "Targeted window {} to be switched doesn't exist".window)

    def switch_to_frame(self, framename):
        """Switch focus to the specified frame.

        :param framename: name of the frame to switch.
        """
        self.page_readiness_wait()
        try:
            self.driver.switch_to.frame(framename)
        except selenium_exceptions.NoSuchFrameException:
            AssertionError(
                "Targeted frame {} to be switched doesn't exist".framename)

    def switch_to_frame_by_index(self, index):
        """Switch focus to the specified frame .

        :param framename: index/frame number to switch.
        """
        self.page_readiness_wait()
        try:
            self.driver.switch_to.frame(index)
        except selenium_exceptions.NoSuchFrameException:
            raise AssertionError(
                "Targeted frame {} doesn't exist at passed index".index)

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

    def hover_on_element(self, locator: dict):
        """Hover on a particular element.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :type locator: dict
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            try:
                ActionChains(self.driver).move_to_element(
                    self.__find_element(locator)).perform()
            except selenium_exceptions.NoSuchElementException:
                AssertionError(
                    "Element{} not found".format(locator['by']) +
                    '=' + locator['locatorvalue'])
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
                "Element {} not found".format(
                    locator['by']) + '=' + locator['locatorvalue'])

    def wait_for_element(self, locator) -> bool:
        """Wait for an element to exist in UI.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :rtype: bool
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        try:
            if self.__find_element(locator):
                return True
        except selenium_exceptions.NoSuchElementException:
            AssertionError("Failed to wait for element {}".format(
                locator['by'] + '=' + locator['locatorvalue']))

    def wait_and_accept_alert(self):
        """Wait and accept alert present on the page."""
        try:
            Wait(self.driver, TIME_OUT).until(ec.alert_is_present())
            self.driver.switch_to.alert.accept()
            logger.info("alert accepted")
        except selenium_exceptions.TimeoutException:
            logger.error(
                "Could Not Find Alert Within The Permissible Time Limit")

    def wait_and_reject_alert(self):
        """Wait for alert and rejects."""
        try:
            Wait(self.driver, TIME_OUT).until(ec.alert_is_present())
            self.driver.switch_to.alert.dismiss()
            logger.info("alert dismissed")
        except selenium_exceptions.TimeoutException:
            logger.error(
                "Could Not Find Alert Within The Permissible Time Limit")

    def select_option_by_index(self, locator: dict, index: int):
        """Select the option by index.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param index: integer value for index.
        :type locator: dict
        :type index: int
        """
        self.by_value = locator['by']
        if isinstance(locator, dict) and isinstance(index, int):
            self.locator_check(locator)
            try:
                Select(self.__find_element(locator)).select_by_index(index)
            except selenium_exceptions.NoSuchElementException:
                logger.error("Exception : Element '{}' Not Found".format(
                    locator['by'] + '=' + locator['locatorvalue']))
        else:
            AssertionError(
                "Invalid locator '{}' or index '{}'".format(locator, index))

    def select_option_by_value(self, locator: dict, value: int):
        """Select the option by using value.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param value: string value to select option.
        :type locator: dict
        :type value: int
        """
        self.page_readiness_wait()
        if isinstance(locator, dict) and isinstance(value, int):
            try:
                Select(self.__find_element(locator)).select_by_value(value)

            except selenium_exceptions.NoSuchElementException:
                logger.error("Exception : Element '{}' Not Found".format(
                    locator['by'] + '=' + locator['locatorvalue']))
        else:
            AssertionError(
                "Invalid locator '{}' or value '{}'".format(locator, value))

    def select_option_by_text(self, locator: dict, text):
        """Select the value by using text.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :param text: string value to select option.
        :type locator: dict
        """
        self.page_readiness_wait()
        if isinstance(locator, dict):
            self.locator_check(locator)
            try:
                Select(self.__find_element(locator)
                       ).select_by_visible_text(text)
            except selenium_exceptions.NoSuchElementException:
                logger.error("Exception : Element '{}' Not Found".format(
                    locator['by'] + '=' + locator['locatorvalue']))
        else:
            AssertionError("Invalid locator type")

    def scroll_to_footer(self):
        """Scroll till end of the page."""
        self.page_readiness_wait()
        try:
            self.__execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
        except selenium_exceptions.JavascriptException:
            logger.error('Exception : Not Able to Scroll To Footer')

    def find_elements(self, locator: dict):
        """Return elements matched with locator.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :type locator: dict
        """
        self.locator_check(locator)
        self.page_readiness_wait()
        if isinstance(locator, dict):
            return self.driver.find_elements(
                self.by_value,
                value=locator['locatorvalue'])
        else:
            AssertionError("Invalid locator type")

    def scroll_to_element(self, locator: dict):
        """Scroll to a particular element on the page.

        :param locator: dictionary of identifier type
            and value ({'by':'id', 'value':'start-of-content.'}).
        :type locator: dict
        """
        self.page_readiness_wait()
        if isinstance(locator, dict):
            try:
                self.locator_check(locator)
                element = self.__find_element(locator)
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
            except selenium_exceptions.NoSuchElementException:
                logger.error('Exception : Not Able To Scroll to Element')
            except BaseException:
                self.__execute_script(
                    "arguments[0].scrollIntoView(true)",
                    self.__find_element(locator))
        else:
            AssertionError("Invalid locator type")

    def __find_element(self, locator: dict):
        """Private method simplified finding element.

        :type locator: dict
        """
        if isinstance(locator, dict):
            self.locator_check(locator)
            return self.driver.find_element(
                self.by_value,
                value=locator['locatorvalue'])

    def __execute_script(self, script, web_elm=None):
        """
        Private method to Exeucte the passed script.

        :param script_to_execute: must contain the valid JS to be executed.

        """
        if web_elm is None:
            return self.driver.execute_script(script)
        if isinstance(web_elm, WebElement):
            return self.driver.execute_script(script, web_elm)
        if isinstance(web_elm, dict):
            return self.driver.execute_script(
                script,
                self.__find_element(web_elm))
