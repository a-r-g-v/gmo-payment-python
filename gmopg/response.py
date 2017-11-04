# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals


class Response(object):

    def __init__(self, response_text):
        self.data = self.decode(response_text)
        self.ok = bool('ErrCode' not in self.data)

    def decode(self, response_text):
        import six.moves.urllib.parse as urlparse
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

        return list(result.values())

