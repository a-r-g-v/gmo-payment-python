# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from requests import Session

def make_requests_with_retries():
    # type: () -> Session
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
    session = Session()
    retries = Retry(
        total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session
