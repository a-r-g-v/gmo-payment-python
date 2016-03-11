# coding: utf-8
import unittest
from requests_mock import mock
from gmopg import Tran, API_BASE_URL, ResponseError


class TranTestCase(unittest.TestCase):

    def test_entry(self):
        tran = Tran()

        with mock() as m:
            m.post(API_BASE_URL + 'EntryTran.idPass', text="ErrCode=E01|E01&ErrInfo=E01030002|E01040003")
            self.assertRaises(ResponseError, lambda: tran.entry(options={"JobCd": "CHECK", "ShopID": "1234", "ShopPass": "1234", "OrderID": "test-python-library-1"}))

        with mock() as m:
            m.post(API_BASE_URL + 'EntryTran.idPass', text="AccessID=deadbeefdeadbeefdeadbeefdeadbeef&AccessPass=deadbeefdeadbeefdeadbeefdeadbeef")
            response = tran.entry(options={"JobCd": "CHECK", "ShopPass": "e5sm9fda", "ShopID": "1104314000001", "OrderID": "test-mukasa-py1"})
            assert 'AccessID' in response.data
            assert 'AccessPass' in response.data

    def test_execute(self):
        tran = Tran()

        with mock() as m:
            m.post(API_BASE_URL + 'ExecTran.idPass', text="OrderID=1234&Forward=1234567&Method=0&PayTimes=0&Approve=1234567&TranID=1234&TranDate=20161122112233&CheckString=deadbeef")  # CheckString 確認しても良さそう？
            response = tran.execute(options={"AccessID": "deadbeeed", "AccessPass": "de27d1ab0068f3fdd6d5cc8f98856816", "OrderID": "1234", "CardNo": "1234567890123456", "Expire": "1234"})
            assert 'Approve' in response.data
            assert 'TranID' in response.data
            assert 'TranDate' in response.data
