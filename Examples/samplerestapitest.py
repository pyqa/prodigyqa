"""REST Api Sample Test file."""
from prodigy import ApiTester
import json
import logging
import pytest

# Variable Stack
login_uri = 'https://reqres.in/api/login'
uri = "https://reqres.in/api/users"
credentials = {"email": "peter@klaven",
               "password": "cityslicka"}
payload = {"name": "morpheus",
           "job": "leader"}
header = {'Accept': 'application/json',
          'Content-Type': 'application/json'}


class TestClass(ApiTester):
    """Sample Test Suite."""
    @pytest.mark.get
    def test_get_users(self):
        """Get users from application."""
        users = self.apirequest(method="GET", url=uri)
        resp = json.loads(users.text)
        logging.info(resp)
        self.assert_in_resp(resp=resp, member='orge',
                            container='resp.data.0.first_name')
        self.assert_equal_resp(resp=resp, member='George',
                               container='resp.data.0.first_name')
        self.assert_not_equal_resp(resp=resp, member='George1',
                                   container='resp.data.0.first_name')
        self.assert_not_in_resp(resp=resp, member='John',
                                container='resp.data.0.first_name')

    @pytest.mark.post
    def test_post_users(self):
        """Create users."""
        users = self.apirequest(method="post", url=uri, data=payload)
        resp = json.loads(users.text)
        logging.warning(resp)
        self.assert_not_in_resp(resp, member='2018-11-20', container='resp.createdAt')

