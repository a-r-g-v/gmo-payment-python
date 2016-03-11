import simplejson as json
import requests

API_BASE_URL = ''
DEFAULT_TIMEOUT = 30


class Error(Exception):
    pass


class BaseAPI(object):

    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self.timeout = timeout

    def _requests(self, method, path, **kwargs):

        response = method(API_BASE_URL + path, timeout=self.timeout, **kwargs)

        response.raise_for_status()

        # TODO: Check Error
        return response

    def get(self, path, **kwargs):
        return self._requests(requests.get, path, **kwargs)

    def post(self, path, **kwargs):
        return self._requests(requests.post, path, **kwargs)


class Tran(BaseAPI):
    pass


class Member(BaseAPI):
    pass


class Card(BaseAPI):
    pass


class Trade(BaseAPI):
    pass
