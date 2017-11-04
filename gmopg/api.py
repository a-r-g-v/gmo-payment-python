# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from gmopg.exceptions import ResponseError
from gmopg._helpers import make_requests_with_retries
from gmopg.response import Response

class BaseAPI(object):
    API_BASE_URL_PRODUCTION = 'https://p01.mul-pay.jp/payment/'
    API_BASE_URL_DEVELOPMENT = 'https://pt01.mul-pay.jp/payment/'
    DEFAULT_TIMEOUT = 30

    def __init__(self, timeout=None, production=True):

        if timeout:
            self.timeout = timeout
        else:
            self.timeout = self.DEFAULT_TIMEOUT

        self.api_base_url = self.API_BASE_URL_PRODUCTION if production else self.API_BASE_URL_DEVELOPMENT

    def _requests(self, method, path, **kwargs):

        response = method(self.api_base_url + path, timeout=self.timeout, **kwargs)

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
