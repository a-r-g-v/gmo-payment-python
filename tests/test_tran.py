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
