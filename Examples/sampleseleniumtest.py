"""Sample test scripts for selenium pytest sample."""

from imgqa import BrowserActions


class Login:
    """hold all locators for POM style implementation."""

    base_url = "https://example.com/"
    login_btn = {"locatorvalue": '//*[@id="menu-item-15255"]/a',
                 "by": "By.XPATH"}
    username = {"locatorvalue": 'username',
                "by": "By.ID", "value": "alpha"}
    password = {"locatorvalue": 'password',
                "by": "By.ID", "value": "alpha"}
    login_button = {"locatorvalue": 'loginButton', "by": "By.ID"}


class TestClass(BrowserActions):
    """Test Class Container for test cases."""
    def login(self, username_dict=None,
              password_dict=None,
              login_button=None):
        self.send_keys(username_dict)
        self.send_keys(password_dict)
        self.click(login_button)

    def test_googlesearch1(self):
        """Just to Open www.google.com and search a list."""
        self.open(Login.base_url)
        self.maximize()
        self.click(Login.login_btn)
        self.login(username_dict=Login.username,
                   password_dict=Login.password,
                   login_button=Login.login_button)
