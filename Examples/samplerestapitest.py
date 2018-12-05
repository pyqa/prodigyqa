"""REST Api Sample Test file."""
from imgqa.core.restapitester import RestApiTester
import json
import logging

# Variable Stack
login_uri = 'https://reqres.in/api/login'
uri = "https://reqres.in/api/users"
credentials = {"email": "peter@klaven",
               "password": "cityslicka"}
payload = {"name": "morpheus",
           "job": "leader"}
header = {'Accept': 'application/json',
          'Content-Type': 'application/json'}


class TestClass(RestApiTester):
    """Sample Test Suite."""

    def test_get_users(self):
        """Get users from application."""
        users = self.apirequest(method="GET", url=uri)
        resp = json.loads(users.text)
        logging.warning(resp)
        self.assert_not_in_resp(resp=resp, member='Georg1e',
                                container='resp.data.0.first_name')

    def test_post_users(self):
        """Create users."""
        users = self.apirequest(method="post", url=uri, data=payload)
        resp = json.loads(users.text)
        logging.warning(resp)
        self.assert_in_resp(resp, member='2018-11-20',
                            container='resp.createdAt')
