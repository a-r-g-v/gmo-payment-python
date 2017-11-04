# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from gmopg.api import Tran, Card, Member, Trade
from gmopg.exceptions import ResponseError, GMOPGException
from gmopg.context import Context


__all__ = ["GMOPG", "ResponseError", "GMOPGException"]

class GMOPG(object):
    def __init__(self, timeout=None, production=True):
        self._context = Context(timeout=timeout, production=production)
        self.tran = Tran(context=self._context)
        self.card = Card(context=self._context)
        self.member = Member(context=self._context)
        self.trade = Trade(context=self._context)
