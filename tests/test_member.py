# confing: utf-8
import unittest
from requests_mock import mock
from gmopg.api import Member 

class MemberTestCase(unittest.TestCase):

    def test_save(self):
        member = Member()

        with mock() as m:
            m.post(member.api_base_url + 'SaveMember.idPass', text="MemberID=1234")
            response = member.save(options={"SiteID": "1234", "SitePass": "1234", "MemberID": "1234"})
            assert 'MemberID' in response.data
            assert response.data['MemberID'] == '1234'

    def test_update(self):
        member = Member()

        with mock() as m:
            m.post(member.api_base_url + 'UpdateMember.idPass', text="MemberID=1234")
            response = member.update(options={"SiteID": "1234", "SitePass": "1234", "MemberID": "1234", "MemberName": "poe"})
            assert 'MemberID' in response.data
            assert response.data['MemberID'] == '1234'

    def test_delete(self):
        member = Member()

        with mock() as m:
            m.post(member.api_base_url + 'DeleteMember.idPass', text="MemberID=1234")
            response = member.delete(options={"SiteID": "1234", "SitePass": "1234", "MemberID": "1234", "MemberName": "poe"})
            assert 'MemberID' in response.data
            assert response.data['MemberID'] == '1234'

    def test_search(self):
        member = Member()

        with mock() as m:
            m.post(member.api_base_url + 'SearchMember.idPass', text="MemberID=1234&MemberName=1234&DeleteFlag=0")
            response = member.search(options={"SiteID": "1234", "SitePass": "1234", "MemberID": "1234"})
            assert 'MemberID' in response.data
            assert 'MemberName' in response.data
            assert 'DeleteFlag' in response.data
