# coding: utf-8
import unittest
from requests_mock import mock
from gmopg import Card, API_BASE_URL


class CardTestCase(unittest.TestCase):

    def test_save(self):
        card = Card()

        with mock() as m:
            m.post(API_BASE_URL + 'SaveCard.idPass', text="CardSeq=1000&CardNo=1111111111&Forward=1111111")
            response = card.save(options={'SiteID': '1234', 'SitePass': '1234', 'MemberID': '1', 'CardNo': '1111111111', 'Expire': '1111'})
            assert 'CardSeq' in response.data
            assert 'CardNo' in response.data
            assert 'Forward' in response.data
