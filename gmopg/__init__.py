# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from gmopg.api import Tran, Card, Member, Trade
from gmopg.exceptions import ResponseError, GMOPGException


__all__ = ["GMOPG", "ResponseError", "GMOPGException"]

class GMOPG(object):
    def __init__(self, timeout=None, production=True):
        self.tran = Tran(timeout=timeout, production=production)
        self.card = Card(timeout=timeout, production=production)
        self.member = Member(timeout=timeout, production=production)
        self.trade = Trade(timeout=timeout, production=production)


