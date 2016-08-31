#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2016 Bitquant Research Laboratories (Asia) Limited
#
# Released under Simplified BSD License
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

from backtrader.feeds import feed
from backtrader.utils import date2num


class SharpPointCSVData(feed.CSVDataBase):
    '''
    Parses a self-defined CSV Data used for testing.

    Specific parameters:

      - ``dataname``: The filename to parse or a file-like object
      - ``product`` : Product id
    '''
    params = (('product', None),)
    def _load(self):
        if self.f is None:
            return False

        # Let an exception propagate to let the caller know
        while True:
            line = self.f.readline()
            if not line:
                return False
            line = line.rstrip('\n')
            print(line)
            linetokens = line.split(self.separator)
            if linetokens[4] == self.p.product:
                return self._loadline(linetokens)

    def _loadline(self, linetokens):
        itoken = iter(linetokens)

        price = float(next(itoken))
        volume = float(next(itoken))
        dtnum = float(next(itoken))
        dt = datetime.datetime.fromtimestamp(dtnum)
        self.lines.datetime[0] = date2num(dt)
        self.lines.open[0] = price
        self.lines.high[0] = price
        self.lines.low[0] = price
        self.lines.close[0] = price
        self.lines.volume[0] = volume
        self.lines.openinterest[0] = 0.0
        print(self.lines)
        return True


class SharpPointCSV(feed.CSVFeedBase):
    DataCls = SharpPointCSVData
