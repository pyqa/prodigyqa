
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
| verify  | optional  | Either a boolean, in which case it controls whether we verify the server’s TLS certificate, or a string, in which case it must be a path to a CA bundle to use. Defaults to True. |
| stream  | optional  | if False, the response content will be immediately downloaded. |
| cert  | optional  | if String, path to ssl client cert file (.pem). If Tuple, (‘cert’, ‘key’) pair. |
