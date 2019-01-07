
Browser Actions Module method Summary 
---
This module adds a wrapper around selenium web driver functions. This inherits Python's unittest.TestCase class and runs with Pytest.
Below are the major areas handled in this module:
* Most frequently, a DOM refresh will cause an exception (StaleElementReferenceException) if the object is changing state.  we are handling this by checking Web Page Expected to be in the ready state and Catch the exception to prevent a failure if the object is not present in web page after web page is in the expected state.
* Version controlling also easily handled without changing test suites.
* The default timeout for finding web elements is 10 seconds, even user also can pass timeout as input parameter to this wrapper functions.
* Most of the functions of this module will Catch the exception to prevent a failure.

| Method Name | Description | Args | Usage |
|---|---|---|---|
| page_readiness_wait | Web Page Expected to be in ready state. |  | self.page_readiness_wait(self) |
| locator_check | Local Method to classify the type of locator. | (a)locator_dict: dictionary of locator value, locator by and value | self.locator_check(self, locator_dict) |
| open | Open the passed 'url'. |  | self.open(self, url) |
| reload_page | Method to refresh the page by selenium or java script. |  | self.reload_page(self) |
| get_page_source | Return the entire HTML source of the current page or frame. |  | self.get_page_source(self) |
| get_title | Return the title of current page.|  | self.get_title(self)|
| get_location | Return the current browser URL using Selenium/Java Script.|  | self.get_location(self) |
| get_attribute | Fetch attribute from provided locator.| (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) attribute_name: attribute name to get it's value | self.get_attribute(self, locator, attribute_name=None)|
| click | Click an element. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.click(self, locator) |
| send_keys | Send text but does not clear the existing text. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) string to send. | self.send_keys(self, locator) |
| get_text | Get text from provided Locator. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.get_text(self, locator) |
| go_back | Simulate back button on browser using selenium or js. |  | self.go_back(self) |
| go_forward | Simulate forward button on browser using  selenium or js. |  | self.go_forward(self) |
| set_window_size | Set width and height of the current window. (window.resizeTo) | (a) width: the width in pixels to set the window to. (b) height: the height in pixels to set the window to. | self.set_window_size(800,600) |
| maximize | Maximize the current window. |  | self.maximize(self) |
| get_driver_name | Return the name of webdriver instance. |  | self.get_driver_name(self) |
| get_domain_url | Method to extract domain url from webdriver itself. |  | self.get_domain_url(self) |
| clear_text | Clear the text if it's a text entry element | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.clear_text(self, locator) |
| capture_screenshot | Save screenshot to the directory(existing or new one). | (a) filepath: file name with directory path(C:/images/image.png). | self.capture_screenshot(self, filepath) |
| switch_to_active_element | Return the element with focus, or BODY if nothing has focus. |  | self.switch_to_active_element(self) |
| switch_to_window | Switch focus to the specified window using selenium/javascript. | (a) name of the window to switch | self.switch_to_window(self, window) |
| switch_to_frame | Switch focus to the specified frame using selenium/javascript. | (a) framename: name of the frame to switch. | self.switch_to_frame(self, framename) |
| switch_to_default_content | Switch focus to the default frame. |  | self.switch_to_default_content(self) |
| switch_to_alert | Switch focus to an alert on the page. |  | self.switch_to_alert(self) |
| hover_on_element | Hover on a particular element. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.hover_on_element(self, locator) |
| hover_on_click | Hover & click a particular element. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.hover_on_click(self, locator) |
| wait_for_element | Wait for an element to exist in UI. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.wait_for_element(self, locator) |
| wait_and_accept_alert | Wait and accept alert present on the page. |  | self.wait_and_accept_alert(self) |
| wait_and_reject_alert | Wait for alert and rejects. |  | self.wait_and_reject_alert(self) |
| select_option_by_index | Select the option by index. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) index: integer value for index. | self.select_option_by_index(self, locator, index) |
| select_option_by_value | Select the option by using value. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) value: string value to select option. | self.select_option_by_value(self, locator, value) |
| select_option_by_text | Select the value by using text. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) text: string value to select option. | self.select_option_by_text(self, locator, text) |
| scroll_to_footer | Scroll till end of the page. |  | self.scroll_to_footer(self) |
| scroll_to_element | Scroll to a particular element on the page. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.scroll_to_element(self, locator) |
| find_elements | Return elements matched with locator. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.find_elements(self, locator) |
