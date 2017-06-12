# coding: utf-8
import six.moves.urllib.parse as urlparse
from errors import Error
from requests import Session

API_BASE_URL_PRODUCTION = 'https://p01.mul-pay.jp/payment/'
API_BASE_URL_DEVELOPMENT = 'https://pt01.mul-pay.jp/payment/'

DEFAULT_TIMEOUT = 30

def make_requests_with_retries():
    # type: () -> Session
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
    session = Session()
    retries = Retry(
        total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session


class ResponseError(Exception):

    def __init__(self, response):
        self.error = self.parse(response.data)

    def __str__(self):
        return "Response contains Error: " + repr(self.error)

    def __repr__(self):
        return self.__str__()

    def parse(self, response):
        dict_list = [Error(i).to_dict() for i in response['ErrInfo'].split('|')]
        return {k: v for dic in dict_list for k, v in dic.items()}


class Response(object):

    def __init__(self, response_text):
        self.data = self.decode(response_text)
        self.ok = bool('ErrCode' not in self.data)

    def decode(self, response_text):
        response_dict = urlparse.parse_qs(response_text)
        return {k: v[0] for k, v in response_dict.items()}

    def parse(self, ignores=[]):
        assert type(self.data) is dict
        assert type(ignores) is list

        result = {}
        for k, v in self.data.items():
            if k in ignores:
                continue

            for i2, v2 in enumerate(str(v).split('|')):
                if i2 not in result:
                    result[i2] = {}
                result[i2][k] = v2

        return result.values()


class BaseAPI(object):

    def __init__(self, timeout=DEFAULT_TIMEOUT, production=True):
        self.timeout = timeout
        self.api_base_url = API_BASE_URL_PRODUCTION if production else API_BASE_URL_DEVELOPMENT

    def _requests(self, method, path, **kwargs):

        response = method(self.api_base_url + path, timeout=self.timeout, **kwargs)

        response.raise_for_status()

        response = Response(response.text)

        if not response.ok:
            raise ResponseError(response)

        return response

    def get(self, path, **kwargs):
        requests = make_requests_with_retries()
        return self._requests(requests.get, path, **kwargs)

    def post(self, path, **kwargs):
        requests = make_requests_with_retries()
        return self._requests(requests.post, path, **kwargs)

    def assertRequiredOptions(self, key, options):
        for i in key:
            assert i in options


class Member(BaseAPI):

    def save(self, options={}):
        self.assertRequiredOptions(["SiteID", "SitePass", "MemberID"], options)
        return self.post("SaveMember.idPass", data=options)

    def update(self, options={}):
        self.assertRequiredOptions(["SiteID", "SitePass", "MemberID"], options)
        return self.post("UpdateMember.idPass", data=options)

    def delete(self, options={}):
        self.assertRequiredOptions(["SiteID", "SitePass", "MemberID"], options)
        return self.post("DeleteMember.idPass", data=options)

    def search(self, options={}):
        self.assertRequiredOptions(["SiteID", "SitePass", "MemberID"], options)
        return self.post("SearchMember.idPass", data=options)


class Card(BaseAPI):

    def save(self, options={}):
        self.assertRequiredOptions(['SiteID', 'SitePass', 'MemberID', 'CardNo', 'Expire'], options)
        return self.post('SaveCard.idPass', data=options)

    def delete(self, options={}):
        self.assertRequiredOptions(['SiteID', 'SitePass', 'MemberID', 'CardSeq'], options)
        return self.post('DeleteCard.idPass', data=options)

    def search(self, options={}):
        self.assertRequiredOptions(['SiteID', 'SitePass', 'MemberID', 'SeqMode'], options)
        return self.post('SearchCard.idPass', data=options)

    def traded(self, options={}):
        self.assertRequiredOptions(['ShopID', 'ShopPass', 'OrderID', 'SiteID', 'SitePass', 'MemberID'], options)
        return self.post('TradedCard.idPass', data=options)


class Trade(BaseAPI):

    def search(self, options={}):
        self.assertRequiredOptions(['ShopID', 'ShopPass', 'OrderID'], options)
        return self.post('SearchTrade.idPass', data=options)


class Tran(BaseAPI):

    def entry(self, options={}):
        # TODO 3D セキュア系は後で実装する

        self.assertRequiredOptions(['ShopID', 'ShopPass', 'OrderID', 'JobCd'], options)
        assert options["JobCd"] == "CHECK" or options["Amount"] is not None

        return self.post('EntryTran.idPass', data=options)

    def execute(self, options={}):
        self.assertRequiredOptions(['AccessID', 'AccessPass', 'OrderID'], options)
        assert ('Method' not in options or options['Method'] % 2 != 0) or 'PayTimes' in options

        return self.post('ExecTran.idPass', data=options)

    def change(self, options={}):
        self.assertRequiredOptions(['ShopID', 'ShopPass', 'AccessID', 'AccessPass', 'JobCd', 'Amount'], options)
        return self.post('ChangeTran.idPass', data=options)

    def alter(self, options={}):
        self.assertRequiredOptions(['ShopID', 'ShopPass', 'AccessID', 'AccessPass', 'JobCd'], options)
        return self.post('AlterTran.idPass', data=options)


class GMOPG(object):

    def __init__(self, timeout=DEFAULT_TIMEOUT, production=True):
        self.tran = Tran(timeout=timeout, production=production)
        self.card = Card(timeout=timeout, production=production)
        self.member = Member(timeout=timeout, production=production)
        self.trade = Trade(timeout=timeout, production=production)
