# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

class Context(object):
    API_BASE_URL_PRODUCTION = 'https://p01.mul-pay.jp/payment/'
    API_BASE_URL_DEVELOPMENT = 'https://pt01.mul-pay.jp/payment/'
    DEFAULT_TIMEOUT = 30

    def __init__(self, timeout=None, production=True):
        if timeout:
            self.timeout = timeout
        else:
            self.timeout = self.DEFAULT_TIMEOUT

        self.api_base_url = self.API_BASE_URL_PRODUCTION if production else self.API_BASE_URL_DEVELOPMENT
