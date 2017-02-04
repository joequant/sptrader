"""Base class for spstrategy classes"""
###############################################################################
#
# Copyright (C) 2016 Bitquant Research Laboratories (Asia) Limited
#
# Licensed under the Simplified BSD License
#
###############################################################################

import sys  # To find out the script name (in argv[0])
import logging
import backtrader as bt
import inspect
import spreport

# Create a Strategy

class SharpPointStrategy(bt.Strategy):
    params = (
        ('log', sys.stdout),
        ('loglevel', logging.INFO),
        ('report', "debug"),
        ('id', None),
        ('tickersource', None),
        ('dataname', None),
        ('loglevel_default', logging.INFO),
        ('order_mode', "active")
    )

    headers =  [
        {'headerName': "Loglevel",
         'field': "loglevel"},
        {'headerName': "Report",
         'field': "report",
         'select' : ["debug", "trade"]},
        {'headerName': "Order Mode",
         'field': "order_mode",
         'select' : ["active", "inactive"]}
        ]

    def __init__(self):
        super().__init__()
        self.report = spreport.report_list[self.p.report](self)
        self.set_tradehistory(True)

    @classmethod
    def header_list(cls):
        a = []
        for base_class in inspect.getmro(cls):
            if issubclass(base_class, SharpPointStrategy):
                a[:0] = base_class.headers
        return a

    def log(self, *args, dt=None, level=None):
        self.report.log(*args, dt=dt, level=level)

    def buy(self, **kwargs):
        kwargs['Ref'] = self.p.id
        if self.p.order_mode == "inactive":
            kwargs['Inactive'] = 1
        else:
            kwargs['Inactive'] = 0
        self.report.buy(kwargs)
        return super().buy(**kwargs)

    def sell(self, **kwargs):
        kwargs['Ref'] = self.p.id
        if self.p.order_mode == "inactive":
            kwargs['Inactive'] = 1
        else:
            kwargs['Inactive'] = 0
        self.report.sell(kwargs)
        return super().sell(**kwargs)

    def notify_order(self, order):
        self.report.notify_order(order)

    def notify_trade(self, trade):
        self.report.notify_trade(trade)

    def next(self):
        raise NotImplementedError
