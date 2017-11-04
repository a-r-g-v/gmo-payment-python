# coding: utf-8
import unittest
from requests_mock import mock
from gmopg.api import Trade

class TradeTestCase(unittest.TestCase):

    def test_search(self):
        trade = Trade()

        with mock() as m:
            m.post(trade.API_BASE_URL_PRODUCTION + 'SearchTrade.idPass', text="Status=SAUTH&ProcessDate=20110101011111&JobCd=SAUTH&AccessID=1234&AccessPass=1234&Amount=1234&Tax=1234&SiteID=1234&MemberID=1234&CardNo=1234&Expire=1122&Mehotd=1&Forward=111&TranID=1234&Approve=1234")
            response = trade.search(options={'ShopID': '1234', 'ShopPass': '1234', 'OrderID': '1234'})
            assert 'CardNo' in response.data
            assert 'Status' in response.data
