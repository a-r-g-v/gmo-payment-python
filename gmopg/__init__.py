# coding: utf-8
import requests
import urlparse
from errors import Error

API_BASE_URL = 'https://p01.mul-pay.jp/payment/'
DEFAULT_TIMEOUT = 30


class ResponseError(Exception):

    def __init__(self, response):
        self.error = self.parse(response.data)

    def __str__(self):
        return "Response contains Error" + repr(self.error)

    def __repr__(self):
        return self.__str__()

    def parse(self, response):
        return [Error(i) for i in response['ErrInfo'][0].split('|')]


class Response(object):

    def __init__(self, response_text):
        self.data = self.decode(response_text)
        self.ok = bool('ErrCode' not in self.data)

    def decode(self, response_text):
        return urlparse.parse_qs(response_text)


class BaseAPI(object):

    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self.timeout = timeout

    def _requests(self, method, path, **kwargs):

        response = method(API_BASE_URL + path, timeout=self.timeout, **kwargs)

        response.raise_for_status()

        print response.text
        # assert False

        response = Response(response.text)

        if not response.ok:
            raise ResponseError(response)

        return response

    def get(self, path, **kwargs):
        return self._requests(requests.get, path, **kwargs)

    def post(self, path, **kwargs):
        return self._requests(requests.post, path, **kwargs)

    def assertRequiredOptions(self, key, options):
        for i in key:
            assert i in options


class Member(BaseAPI):
    pass


class Card(BaseAPI):
    pass


class Trade(BaseAPI):
    pass


class Tran(BaseAPI):

    def entry(self, options={}):
        """
            取引登録 API
            これ以降の決済取引で必要となる取引 ID と取引パスワードの発行を行い、取引を開始します。

            ShopID  char(13)
            ShopPass    char(10)
            OrderID char(27)    取引を識別するID
            JobCd   char    処理区分 CHECK / CAPTURe / AUTH / SAUTH
            Amount  number(7)   処理区分が有効性チェック(CHECK)を除き必須，利用金額
            Tax number(7) 税送料
            TdFlag char(1)  本人認証サービスを使用するかどうか 0 or 1
            TdTenantName    char    3Dセキュア表示店舗名
        """
        # TODO 3D セキュア系は後で実装する

        self.assertRequiredOptions(['ShopID', 'ShopPass', 'OrderID', 'JobCd'], options)
        assert options["JobCd"] == "CHECK" or options["Amount"] is not None

        return self.post('EntryTran.idPass', data=options)


class GMOPG(object):

    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self.tran = Tran(timeout=timeout)
