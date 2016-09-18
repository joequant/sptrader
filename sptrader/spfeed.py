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
import time
import spstore
from backtrader.feeds import feed
from backtrader.utils import date2num
from backtrader.metabase import MetaParams
from backtrader.utils.py3 import with_metaclass

class MetaSharpPointData(feed.MetaCSVDataBase):
    def __init__(cls, name, bases, dct):
        '''Class has already been created ... register'''
        # Initialize the class
        super(MetaSharpPointData, cls).__init__(name, bases, dct)
        spstore.SharpPointStore.DataCls = cls


class SharpPointCSVData(with_metaclass(MetaSharpPointData, feed.CSVDataBase)):
    '''
    Parses a self-defined CSV Data used for testing.

    Specific parameters:

      - ``dataname``: The filename to parse or a file-like object
      - ``product`` : Product id
    '''
    params = (('nullvalue', float('NaN')),
              ('product', None),
              ('newdata', False),
              ('keepalive', False),
              ('debug', True),
              ('streaming', False))

    def __init__(self, **kwargs):
        super(SharpPointCSVData, self).__init__()
        self.o = spstore.SharpPointStore(**kwargs)

    def start(self):
        super(SharpPointCSVData, self).start()
        if self.p.newdata:
            self.f.seek(0, 2)
            self.forward()
            dt = datetime.datetime.now()
            self.lines.datetime[0] = date2num(dt)
            self.lines.open[0] = self.p.nullvalue
            self.lines.high[0] = self.p.nullvalue
            self.lines.low[0] = self.p.nullvalue
            self.lines.close[0] = self.p.nullvalue
            self.lines.volume[0] = self.p.nullvalue
            self.lines.openinterest[0] = self.p.nullvalue
        if self.p.streaming:
            print("start price streaming")
            self.o.streaming_prices(self.p.product)

    def _load(self):
        if self.f is None:
            return False

        # Let an exception propagate to let the caller know
        while True:
            line = self.f.readline()
            if not line:
                if not self.p.keepalive:
                    return False
                else:
                    time.sleep(0.1)
                    continue
            else:
                line = line.rstrip('\n')
                if self.p.debug:
                    print(line)
                linetokens = line.split(self.separator)
                if linetokens[4] == self.p.product:
                    return self._loadline(linetokens)

    def islive(self):
        return self.p.keepalive

    def product(self):
        return self.p.product

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
        return True


class SharpPointCSV(feed.CSVFeedBase):
    DataCls = SharpPointCSVData
