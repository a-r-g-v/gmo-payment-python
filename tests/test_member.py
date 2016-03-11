# confing: utf-8
import unittest
from requests_mock import mock
from gmopg import Member, API_BASE_URL


class MemberTestCase(unittest.TestCase):

    def test_save(self):
        member = Member()

        with mock() as m:
            m.post(API_BASE_URL + 'SaveMember.idPass', text="MemberID=1234")
            response = member.save(options={"SiteID": "1234", "SitePass": "1234", "MemberID": "1234"})
            assert 'MemberID' in response.data
            assert response.data['MemberID'] == '1234'

    def test_update(self):
        member = Member()

        with mock() as m:
            m.post(API_BASE_URL + 'UpdateMember.idPass', text="MemberID=1234")
            response = member.update(options={"SiteID": "1234", "SitePass": "1234", "MemberID": "1234", "MemberName": "poe"})
            assert 'MemberID' in response.data
            assert response.data['MemberID'] == '1234'
