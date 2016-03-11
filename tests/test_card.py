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

    def test_delete(self):
        card = Card()
        with mock() as m:
            m.post(API_BASE_URL + 'DeleteCard.idPass', text="CardSeq=1000")
            response = card.delete(options={'SiteID': '1234', 'SitePass': '1234', 'MemberID': '1', 'CardSeq': '1000'})
            assert 'CardSeq' in response.data

    def test_search(self):
        card = Card()
        with mock() as m:
            m.post(API_BASE_URL + 'SearchCard.idPass', text="CardSeq=1|2&DefaultFlag=1|0&CardName=poe|foo&CardNo=1234|2345&Expire=1111|1112&HolderName=poe|foo&DeleteFlag=1|0")
            response = card.search(options={'SiteID': '1234', 'SitePass': '1234', 'MemberID': '1234', 'SeqMode': '1'})

            parased_response = response.parse(ignores=['DeleteFlag'])
            assert type(parased_response) is list
            assert len(parased_response) == 2
            assert parased_response[0]['CardSeq'] == '1'
            assert parased_response[0]['CardName'] == 'poe'

            assert parased_response[1]['CardSeq'] == '2'
            assert parased_response[1]['CardName'] == 'foo'

    def test_traded(self):
        card = Card()
        with mock() as m:
            m.post(API_BASE_URL + 'TradedCard.idPass', text="CardSeq=1&CardNo=1111&Forward=1111")
            response = card.traded(options={'SiteID': '1111', 'SitePass': '1111', 'OrderID': '1234', 'ShopID': '1234', 'ShopPass': '1234', 'MemberID': '1234'})
            assert 'CardNo' in response.data
