[![Waffle.io - Columns and their card count](https://badge.waffle.io/pyqa/imgqa.svg?columns=all)](https://waffle.io/pyqa/imgqa)
[![Build Status](https://travis-ci.org/pyqa/imgqa.svg?branch=master)](https://travis-ci.org/pyqa/imgqa)
[![PyPI version](https://badge.fury.io/py/imgqa.svg)](https://badge.fury.io/py/imgqa)

# QA automation framework - QA Re-Imagined!

QA-ReImagined a.k.a `IMGQA` is a unified test automation framework based on python. This has come up after thoroughly study made on existing methodologies used in majority of projects for UI/Rest API testing, This is expected to solve a list of problem statements readily.
The framework aims to be a constructive blend of various guidelines, coding standards, concepts, processes, practices, project hierarchies, modularity, reporting mechanism, test data injections etc., to pillar automation testing.


## Key Features

- **Selenium functions:** This module contains a good number of Selenium wrapped functions which are commonly used for UI Testing. These wrapped functions provide a shield of exception handling over the regular selenium methods, handling all different kinds of exception that can occur. If due to some reason, any of the provided method doesnot work, then there is a provision of fall back mechanism, provided in each method, by leveraging additional technologies/javascript 
 
- **Rest API functions:** This module contains Rest API wrapped functions which are commonly used for Rest API Testing, by leveraging python 'requests' library. The methods are generalized, to handle any kind of request like GET, PUT, POST, DELETE etc. The module has provison to manage the authentication token. Additionally, there are generic methods for commonly used assertion types and for validating the parameters, that come along with a request like headers, payload etc. in a most possible simplified manner
 
- **Utilities:** This module aims to provide community backed utility libraries built with a focus on reusability. Following are the utilities, currently supported by the framework:  
    - **Image Comparison:** This module provides provision for image comparison through openCV, SSIM(Structured similarity index) as opposed to pixel by pixel comparison. The methods are generic and need just 2 images to compute the difference. 
     
    - **Captcha Reading:** This utility performs the captcha reading from an image, by leveraging the 'pytesseract' module. It takes an image as input, containing captcha, and returns a string, mentioning the captcha.
     
    - **Spell Check, Accessibility Check in web application:** This module is in WIP mode, where we are enabling spell checks and accessibility checks in web applications, by leveraging the web spider concept, which browses the World Wide Web in a methodical, automated manner, takes out all the links from a web page so that the process could be repeated.

- **Reporting:** The framework is flexible enough to work with multiple reporting platforms like `reportportal.io`, `allure-report` etc. A regular, self-contained and customizable HTML report can also be generated through the use of `pytest-html` module.(which is bundled as a dependency for this package)
 
- **Continuous Testing:** The framework provides the facility for CT(Continuous Testing) by leveraging Docker. The docker file provided in the framework can be used to setup the necessary prerequisites/environment, needed to run the framework, on any server, from scratch. 

## Prerequisites

The framework requires 
- [python 2.7+ / 3.6+](https://www.python.org/downloads/)
- [pip](pip )
- [pytest](https://docs.pytest.org/en/latest/getting-started.html) to be installed in the machine.

## Installing

Valid/Tested Version is suggested to be installed directly from PyPi as it will solve the issue of dependencies automatically.

`pip install imgqa`

In case of any custom updates done to the current setup,we will need to clone the current repository and run `python setup.py develop` so that the local changes are reflected in the install version.


## Running the tests

The sample test cases for all the features are listed under **imgqa --> Examples** folder. To run the sample tests, open command prompt/terminal, go to imgqa --> Examples folder and run the following command:

`pytest {filename}.py -s` (-s indicates the standard output, please refer [here](https://docs.pytest.org/en/latest/contents.html) for a detailed understanding around pytest framework and its features/plugins/options etc.)

## Browser Actions 
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


## API Test Module


REST API Module method Summary 
---

| Method Name | Description | Args | Usage |
|---|---|---|---|
| apirequest | triggers rest api request based on the input method and kwargs | (a).method: GET/POST/PUT/PATCH/DELETE (b).kwargs: Refer below REST API kwarg section table | self.apirequest(method='GET') |
| assert_in_resp | Check whether response data contain input member.| (a)resp: response to validate. (b)member: value to check in response. (c)container: response key path in dot format which should starts with 'resp.'. example: resp.data.0.name | self.assert_in_resp(resp, member, container) |
| assert_not_in_resp | Check whether response data contain input member.| (a)resp: response to validate. (b)member: value to check in response. (c)container: response key path in dot format which should starts with 'resp.'. example: resp.data.0.name | self.assert_not_in_resp(resp, member, container) |
| assert_equal_resp | Check whether response data contain input member.| (a)resp: response to validate. (b)member: value to check in response. (c)container: response key path in dot format which should starts with 'resp.'. example: resp.data.0.name | self.assert_equal_resp(resp, member, container) |
| assert_not_equal_resp | Check whether response data contain input member.| (a)resp: response to validate. (b)member: value to check in response. (c)container: response key path in dot format which should starts with 'resp.'. example: resp.data.0.name | self.assert_not_equal_resp(resp, member, container) |

REST API kwarg section
---

| Arg Name  | Arg type  | Description  |
|---|---|---|
| url  | standard  | API request url |
| params  | optional  | Dictionary, list of tuples or bytes to send in the body of the Request.|
| data  | optional  | Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request. |
| json  | optional  | A JSON serializable Python object to send in the body of the Request. |
| headers  | optional  | Dictionary of HTTP Headers to send with the Request. |
| cookies  | optional  | Dict or CookieJar object to send with the Request. |
| files  | optional  | Dictionary of 'name': file-like-objects(or {'name': file-tuple}) for multipart encoding upload. file-tuple can be a 2-tuple ('filename', fileobj), 3-tuple ('filename', fileobj, 'content_type') or a 4-tuple ('filename', fileobj, 'content_type', custom_headers), where 'content-type' is a string defining the content type of the given file and custom_headers a dict-like object containing additional headers to add for the file. |
| auth  | optional  | Auth tuple to enable Basic/Digest/Custom HTTP Auth. |
| timeout (float or tuple)  | optional  | How many seconds to wait for the server to send data before giving up, as a float, or a (connect timeout, read timeout) tuple. |
| allow_redirects (bool)  | optional  | Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to True. |
| proxies  | optional  | Dictionary mapping protocol to the URL of the proxy. |
| verify  | optional  | Either a boolean, in which case it controls whether we verify the servers TLS certificate, or a string, in which case it must be a path to a CA bundle to use. Defaults to True. |
| stream  | optional  | if False, the response content will be immediately downloaded. |
| cert  | optional  | if String, path to ssl client cert file (.pem). If Tuple, (cert, key) pair. |


