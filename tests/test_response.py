# coding: utf-8
import unittest
from gmopg.response import Response


class ResponseTestCase(unittest.TestCase):

    def test_parse(self):
        response = Response("key1=value1&key2=value2")
        parsed_response = response.parse()
        assert len(parsed_response) == 1
        assert parsed_response[0]['key1'] == "value1"
        assert parsed_response[0]['key2'] == "value2"

        response = Response("key1=value11|value12&key2=value21|value22")
        parsed_response = response.parse()

        assert len(parsed_response) == 2
        assert parsed_response[0]['key1'] == "value11"
        assert parsed_response[1]['key1'] == "value12"
        assert parsed_response[0]['key2'] == "value21"
        assert parsed_response[1]['key2'] == "value22"

        response = Response('key1=value1|value2&key2=poe')
        parsed_response = response.parse()
        assert len(parsed_response) == 2
        assert parsed_response[0]['key2'] == 'poe'

        ignored_parsed_response = response.parse(['key2'])
        assert 'key2' not in ignored_parsed_response[0]
