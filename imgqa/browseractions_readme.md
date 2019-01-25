
Browser Actions Module method Summary 
---
This module wraps around selenium web driver functions. 
Below are the major areas handled in this module:
* Most frequently, a DOM refresh will cause an exception (StaleElementReferenceException) if the object is changing state.  we are handling this by checking Web Page Expected to be in the ready state and Catch the exception to prevent a failure if the object is not present in web page after web page is in the expected state.
* Most of the functions of this module will Catch the exception to prevent a failure.

| Method Name | Description | Args | Usage |
|---|---|---|---|
| page_readiness_wait | Web Page Expected to be in ready state. |  | self.page_readiness_wait() |
| locator_check | Local Method to classify the type of locator. | (a)locator_dict: dictionary of locator value, locator by and value | self.locator_check( locator_dict) |
| open | Open the passed 'url'. |  | self.open(url) |
| reload_page | Method to refresh the page by selenium or java script. |  | self.reload_page() |
| get_page_source | Return the entire HTML source of the current page or frame. |  | self.get_page_source() |
| get_title | Return the title of current page.|  | self.get_title()|
| get_location | Return the current browser URL using Selenium/Java Script.|  | self.get_location() |
| get_attribute | Fetch attribute from provided locator.| (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) attribute_name: attribute name to get it's value | self.get_attribute(locator, attribute_name=None)|
| click | Click an element. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.click(locator) |
| send_keys | Send text but does not clear the existing text. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) string to send. | self.send_keys(locator) |
| get_text | Get text from provided Locator. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.get_text(locator) |
| go_back | Simulate back button on browser using selenium or js. |  | self.go_back() |
| go_forward | Simulate forward button on browser using  selenium or js. |  | self.go_forward() |
| set_window_size | Set width and height of the current window. (window.resizeTo) | (a) width: the width in pixels to set the window to. (b) height: the height in pixels to set the window to. | self.set_window_size(800,600) |
| maximize | Maximize the current window. |  | self.maximize() |
| get_driver_name | Return the name of webdriver instance. |  | self.get_driver_name() |
| get_domain_url | Method to extract domain url from webdriver itself. |  | self.get_domain_url() |
| clear_text | Clear the text if it's a text entry element | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.clear_text(locator) |
| capture_screenshot | Save screenshot to the directory(existing or new one). | (a) filepath: file name with directory path(C:/images/image.png). | self.capture_screenshot(self, filepath) |
| switch_to_active_element | Return the element with focus, or BODY if nothing has focus. |  | self.switch_to_active_element() |
| switch_to_window | Switch focus to the specified window using selenium/javascript. | (a) name of the window to switch | self.switch_to_window(window) |
| switch_to_frame | Switch focus to the specified frame using selenium/javascript. | (a) framename: name of the frame to switch. | self.switch_to_frame(framename) |
| switch_to_default_content | Switch focus to the default frame. |  | self.switch_to_default_content() |
| switch_to_alert | Switch focus to an alert on the page. |  | self.switch_to_alert() |
| hover_on_element | Hover on a particular element. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.hover_on_element(locator) |
| hover_on_click | Hover & click a particular element. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.hover_on_click(locator) |
| wait_for_element | Wait for an element to exist in UI. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.wait_for_element(locator) |
| wait_and_accept_alert | Wait and accept alert present on the page. |  | self.wait_and_accept_alert() |
| wait_and_reject_alert | Wait for alert and rejects. |  | self.wait_and_reject_alert() |
| select_option_by_index | Select the option by index. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) index: integer value for index. | self.select_option_by_index(locator, index) |
| select_option_by_value | Select the option by using value. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) value: string value to select option. | self.select_option_by_value(locator, value) |
| select_option_by_text | Select the value by using text. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). (b) text: string value to select option. | self.select_option_by_text(locator, text) |
| scroll_to_footer | Scroll till end of the page. |  | self.scroll_to_footer() |
| scroll_to_element | Scroll to a particular element on the page. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.scroll_to_element(locator) |
| find_elements | Return elements matched with locator. | (a) locator: dictionary of identifier type and value ({'by':'id', 'value':'start-of-content.'}). | self.find_elements(locator) |
