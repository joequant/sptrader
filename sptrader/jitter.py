#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime, timedelta
import backtrader
from backtrader import TimeFrame
from backtrader.utils.py3 import with_metaclass
from backtrader import metabase


class JitterFilter(with_metaclass(metabase.MetaParams, object)):
    '''
    '''
    params = (('jitter', 5),)
    def __init__(self, data):
        pass

    def __call__(self, data):
        '''
        Return Values:

          - False: data stream was not touched
          - True: data stream was manipulated (bar outside of session times and
          - removed)
        '''
        datadt = data.datetime.datetime()
        newdt = datetime(datadt.year,
                         datadt.month,
                         datadt.day,
                         datadt.hour,
                         datadt.minute,
                         0)
        print(datadt, newdt)
        dseconds = (datadt - newdt).seconds

        if dseconds <= self.p.jitter:
            data.datetime[0] = backtrader.date2num(newdt)
            return True
        return False

       
