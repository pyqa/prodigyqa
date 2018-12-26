# -*- coding: utf-8 -*-
"""Rest API Module."""
import unittest
import requests
import logging
from requests.exceptions import InvalidURL


class ApiTester(unittest.TestCase):
    """REST Api basic methods."""

    def __init__(self, *args, **kwargs):
        """Init Method for webdriver declarations."""
        super(ApiTester, self).__init__(*args, **kwargs)

    def _get_session_token(self, auth_type=None, **kwargs):
        """Input kwargs will change as per application authentication type.

        : param auth_type: (Optional) authorization type for applications api's
            default value is None.
        : param **kwargs: Optional that application request methods takes
            to generate session token.
        """
        if not auth_type:
            pass
        elif auth_type.lower() == "static" and not kwargs["token"]:
            self.token = kwargs["token"]
            return kwargs["token"]
        elif (auth_type.lower() == "dynamic" and
              not kwargs["credentials"] and
              not kwargs["url"]):
            try:
                if self._validate_kwargs(**kwargs) and kwargs['url']:
                    resp = self._post_method(**kwargs)
                    return resp['token']
            except InvalidURL:
                logging.warn("The URL provided was somehow invalid")

    def apirequest(self,
                   method='GET',
                   **kwargs):
        """Send request to class:'request' method object.

        :param method: method for the new :class:'request' method object.
            this method might be either of 'GET', 'POST', 'PUT', 'PATCH'
            and 'DELETE'.
        :param **kwargs: Optional arguments that 'request' method method takes.
        """
        if method.upper() == "GET":
            return self._get_method(**kwargs)

        elif method.upper() == "POST":
            return self._post_method(**kwargs)

        elif method.upper() == "PUT":
            return self._put_method(**kwargs)

        elif method.upper() == "PATCH":
            return self._patch_method(**kwargs)

        elif method.upper() == "DELETE":
            return self._delete_method(**kwargs)

    def _get_method(self, **kwargs):
        r"""Send a GET request.

        :param url: URL for the new :class:'Request' object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the body of the :class:'Request'.
        :param \*\*kwargs: Optional arguments that ''request'' takes.
        :return: :class:'Response <Response>' object
        :rtype: requests.Response
        """
        try:
            if self._validate_kwargs(**kwargs) and kwargs['url']:
                return requests.get(**kwargs)
        except InvalidURL:
            logging.warn("The URL provided was somehow invalid")

    def _post_method(self, **kwargs):
        r"""Send a POST request.

        :param url: URL for the new :class:'Request' object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:'Request'.
        :param json: (optional) json data
            to send in the body of the :class:'Request'.
        :param \*\*kwargs: Optional arguments that ''request'' takes.
        :return: :class:'Response <Response>' object
        :rtype: requests.Response
        """
        try:
            if self._validate_kwargs(**kwargs):
                if kwargs['url']:
                    if (('json' in kwargs and kwargs['json']) or
                            ('data' in kwargs and kwargs['data'])):
                        return requests.post(**kwargs)
        except InvalidURL:
            logging.warn("The URL provided was somehow invalid")

    def _put_method(self, **kwargs):
        r"""Send a PUT request.

        :param url: URL for the new :class:'Request' object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:'Request'.
        :param json: (optional) json data
            to send in the body of the :class:'Request'.
        :param \*\*kwargs: Optional arguments that ''request'' takes.
        :return: :class:'Response <Response>' object
        :rtype: requests.Response
        """
        try:
            if kwargs['url']:
                if (('json' in kwargs and kwargs['json']) or
                        ('data' in kwargs and kwargs['data'])):
                    return requests.put(**kwargs)
        except InvalidURL:
            logging.warn("The URL provided was somehow invalid")

    def _patch_method(self, **kwargs):
        r"""Send a PATCH request.

        :param url: URL for the new :class:'Request' object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:'Request'.
        :param json: (optional) json data
            to send in the body of the :class:'Request'.
        :param \*\*kwargs: Optional arguments that ''request'' takes.
        :return: :class:'Response <Response>' object
        :rtype: requests.Response
        """
        try:
            if kwargs['url']:
                if (('json' in kwargs and kwargs['json']) or
                        ('data' in kwargs and kwargs['data'])):
                    return requests.patch(**kwargs)
        except InvalidURL:
            logging.warn("The URL provided was somehow invalid")

    def _delete_method(self, **kwargs):
        r"""Send a DELETE request.

        :param url: URL for the new :class:'Request' object.
        :param \*\*kwargs: Optional arguments that ''request'' takes.
        :return: :class:'Response <Response>' object
        :rtype: requests.Response
        """
        try:
            if self._validate_kwargs(**kwargs) and kwargs['url']:
                return requests.delete(**kwargs)
        except InvalidURL:
            logging.warn("The URL provided was somehow invalid")

    def _validate_kwargs(self, **kwargs):
        """
        Verify key presence in input kwargs and return the key value.

        standard keywords are defined as per,
        http://docs.python-requests.org/en/master/api/.
        :parm method: method for the new Request object.
        :parm url: URL for the new Request object.
        :parm params: (optional) Dictionary, list of tuples or bytes
            to send in the body of the Request.
        :parm data: (optional) Dictionary, list of tuples, bytes,
            or file-like object to send in the body of the Request.
        :parm json: (optional) A JSON serializable Python object
            to send in the body of the Request.
        :parm headers: (optional) Dictionary of HTTP Headers
            to send with the Request.
        :parm cookies: (optional) Dict or CookieJar object
            to send with the Request.
        :parm files: (optional) Dictionary of 'name': file-like-objects
            (or {'name': file-tuple}) for multipart encoding upload.
            file-tuple can be a 2-tuple ('filename', fileobj),
            3-tuple ('filename', fileobj, 'content_type') or
            a 4-tuple ('filename', fileobj, 'content_type', custom_headers),
            where 'content-type' is a string defining the content type of
            the given file and custom_headers a dict-like object containing
            additional headers to add for the file.
        :parm auth: (optional) Auth tuple
            to enable Basic/Digest/Custom HTTP Auth.
        :parm timeout (float or tuple): (optional) How many seconds
            to wait for the server to send data before giving up, as a float,
            or a (connect timeout, read timeout) tuple.
        :parm allow_redirects (bool): (optional) Boolean.
            Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection.
            Defaults to True.
        :parm proxies: (optional) Dictionary mapping protocol
            to the URL of the proxy.
        :parm verify: (optional) Either a boolean,
            in which case it controls whether we verify the server�s
            TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to True.
        :parm stream: (optional) if False, the response content will be
            immediately downloaded.
        :parm cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, (�cert�, �key�) pair.
        """
        stand_kw = ["method", "url", "params", "data", "json",
                    "headers", "cookies", "files", "auth", "timeout",
                    "allow_redirects", "proxies", "verify", "stream", "cert"]
        try:
            non_stand_kw = [
                key for key in kwargs.keys() if key not in stand_kw]
            if not len(non_stand_kw):
                return True
            else:
                raise KeyError("%s keywords are invalid" % non_stand_kw)
        except KeyError as e:
            logging.warning(e)

    def assert_in_resp(self, resp, member, container):
        """Check whether response data member contain input member.

        :parm resp: response to validate.
        :parm member: value to check in response.
        :parm container: response key path in dot format
            which should starts with 'resp.'. example: resp.data.0.name
        """
        actual_val = self._get_val_from_resp_by_path(resp, container)
        return self.assertIn(member, actual_val)

    def assert_not_in_resp(self, resp, member, container):
        """Check whether response data member doesn't contain input member.

        :parm resp: response to validate.
        :parm member: value to check in response.
        :parm container: response key path in dot format
            which should starts with 'resp.'. example: resp.data.0.name
        """
        actual_val = self._get_val_from_resp_by_path(resp, container)
        return self.assertNotIn(member, actual_val)

    def assert_equal_resp(self, resp, member, container):
        """Check whether response data member is same as input member.

        :parm resp: response to validate.
        :parm member: value to check in response.
        :parm container: response key path in dot format
            which should starts with 'resp.'. example: resp.data.0.name
        """
        actual_val = self._get_val_from_resp_by_path(resp, container)
        return self.assertEqual(member, actual_val)

    def assert_not_equal_resp(self, resp, member, container):
        """Check whether response data member is not same as input member.

        :parm resp: response to validate.
        :parm member: value to check in response.
        :parm container: response key path in dot format
            which should starts with 'resp.'. example: resp.data.0.name
        """
        actual_val = self._get_val_from_resp_by_path(resp, container)
        return self.assertNotEqual(member, actual_val)

    def _get_val_from_resp_by_path(self, resp, path):
        """Get value from response by dot format key path of response .

        :parm resp: response
        :parm path: key path in dot format which should starts with 'resp.'.
            example: resp.data.0.name
        """
        val = ''
        items = path.split('.')
        for index in range(len(items)):
            if index == 0:
                val = items[index]
            else:
                try:
                    val += '[%s]' % int(items[index])
                except ValueError:
                    val += "['%s']" % str(items[index])
        return eval(val)
