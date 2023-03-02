import json
import platform
import threading
from json import JSONDecodeError
from urllib.parse import urlencode, urlsplit, urlunsplit

import requests

from capsolver import error
import capsolver

TIMEOUT_SECS = 600
MAX_CONNECTION_RETRIES = 2

_thread_context = threading.local()


api_key_to_header = (lambda key: {"Authorization": f"Bearer {key}"})


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urlsplit(url)

    if base_query:
        query = "%s&%s" % (base_query, query)

    return urlunsplit((scheme, netloc, path, query, fragment))


def _requests_proxies_arg(proxy):
    """Returns a value suitable for the 'proxies' argument to 'requests.request."""
    if proxy is None:
        return None
    elif isinstance(proxy, str):
        return {"http": proxy, "https": proxy}
    elif isinstance(proxy, dict):
        return proxy.copy()
    else:
        raise ValueError("'capsolver.proxy' must be specified as either a string URL or a dict with string URL under the https and/or http keys.")


def _make_session():
    s = requests.Session()
    proxies = _requests_proxies_arg(capsolver.proxy)
    if proxies:
        s.proxies = proxies
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=MAX_CONNECTION_RETRIES))
    return s


class APIRequestor:
    def __init__(self, key=None, api_base=None):
        self.api_base = api_base or capsolver.api_base
        self.api_key = key or capsolver.api_key

    def request(self, method, url, params=None, headers=None, request_timeout=None):
        result = self.request_raw(method.lower(), url, params=params, supplied_headers=headers, request_timeout=request_timeout)
        resp, rbody, rcode, rheaders = self._interpret_response(result)
        if resp["errorId"]!=0:
            return self.handle_error_response(rbody, rcode, resp, rheaders)
        return resp

    def handle_error_response(self, rbody, rcode, resp, rheaders):
        error_data = resp["errorDescription"]
        if rcode == 429:
            return error.RateLimitError(error_data, rbody, rcode, resp, rheaders)
        elif rcode == 400:
            return error.InvalidRequestError(error_data, rbody, rcode, resp, rheaders)
        elif rcode == 401:
            return error.AuthenticationError(error_data, rbody, rcode, resp, rheaders)
        elif rcode == 403:
            return error.InsufficientCreditError(error_data, rbody, rcode, resp, rheaders)
        elif rcode == 409:
            return error.IncompleteJobError(error_data, rbody, rcode, resp, rheaders)
        else:
            return error.UnknownError(error_data, rbody, rcode, resp, rheaders)

    def request_headers(self, extra):
        user_agent = "capsolver PythonBindings"
        uname_without_node = " ".join(v for k, v in platform.uname()._asdict().items() if k != "node")
        ua = {
            "httplib": "requests",
            "lang": "python",
            "lang_version": platform.python_version(),
            "platform": platform.platform(),
            "publisher": "capsolver",
            "uname": uname_without_node,
        }
        headers = {
            "X-capsolver-Client-User-Agent": json.dumps(ua),
            "User-Agent": user_agent,
        }
        headers.update(api_key_to_header(self.api_key))
        headers.update(extra)
        return headers

    def _validate_headers(self, supplied_headers):
        headers = {}
        if supplied_headers is None:
            return headers
        if not isinstance(supplied_headers, dict):
            raise TypeError("Headers must be a dictionary")
        for k, v in supplied_headers.items():
            if not isinstance(k, str):
                raise TypeError("Header keys must be strings")
            if not isinstance(v, str):
                raise TypeError("Header values must be strings")
            headers[k] = v
        return headers


    def request_raw(self, method, url, *, params=None, supplied_headers=None, request_timeout=None):
        abs_url = "%s%s" % (self.api_base, url)
        headers = self._validate_headers(supplied_headers)
        json_data = {
            "clientKey":self.api_key,
        }
        json_data.update(params)
        headers = self.request_headers(headers)
        if not hasattr(_thread_context, "session"):
            _thread_context.session = _make_session()
        try:
            result = _thread_context.session.request(method, abs_url, headers=headers, json=json_data, timeout=request_timeout if request_timeout else TIMEOUT_SECS)
        except requests.exceptions.Timeout as e:
            raise error.Timeout("Request timed out") from e
        except requests.exceptions.RequestException as e:
            raise error.APIError("Error communicating with capsolver") from e
        return result

    def _interpret_response(self, result):
        return self._interpret_response_line(result.content, result.status_code, result.headers)

    def _interpret_response_line(self, rbody, rcode, rheaders):
        if rcode == 503:
            raise error.ServiceUnavailableError("The server is overloaded or not ready yet.", rbody, rcode, headers=rheaders)
        try:
            if hasattr(rbody, "decode"):
                rbody = rbody.decode("utf-8")
            resp = json.loads(rbody)
        except (JSONDecodeError, UnicodeDecodeError):
            raise error.APIError(f"HTTP code {rcode} from API ({rbody})", rbody, rcode, headers=rheaders)
        return resp, rbody, rcode, rheaders
