'''Sample test scrpits for selenium pytest sample'''

from imgqa.core.pageactions import PageActions


class login_module:
    '''please enusre not to change this class name ,username,password and loin_button if login mechanism is present'''
    base_url = "https://corridor.pramati.com/"
    login_btn = {"locatorvalue": '//*[@id="menu-item-15255"]/a',
                 "by": "By.XPATH"}
    username = {"locatorvalue": 'username',
                "by": "By.ID", "value": "alpha"}
    password = {"locatorvalue": 'password',
                "by": "By.ID", "value": "alpha"}
    login_button = {"locatorvalue": 'loginButton', "by": "By.ID"}


class TestClass(PageActions):

    def login(self, username_dict=None,
              password_dict=None,
              login_button=None):
        """Method for login process."""
        self.wait_for_page_ready_state()
        self.send_keys(username_dict)
        self.send_keys(password_dict)
        self.click(login_button)

    def test_googlesearch1(self):
        """Just to Open www.google.com and search a list."""
        self.open(login_module.base_url)
        self.maximize()
        self.click(login_module.login_btn)
        self.login(username_dict=login_module.username, password_dict=login_module.password,
                   login_button=login_module.login_button)
