"""Implements ImmediateStrategy"""

import sys
import logging
import backtrader as bt
import spstrategy
# Create a Strategy

class ImmediateStrategy(spstrategy.SharpPointStrategy):
    """Immediate strategy automatically executes an order"""
    params = (
        ('qty', 1),
        ('delay', 5),
        ('order', "B"),
        ('log', sys.stdout),
        ('loglevel', logging.INFO)
    )

    @classmethod
    def headers(cls):
        """Headers for web interface"""
        a = super().headers()
        a.extend ([
            {'headerName': "Order",
             'field': "order"},
            {'headerName': "Delay",
             'field': "delay"},
            {"headerName": "Log level",
             "field": "loglevel"}
            ])
        return a

    def __init__(self):
        super().__init__()
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('%.2f %.2f' % (self.datas[0].open[0],
                                self.datas[1].open[0]))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if len(self.datas[0].close) > self.p.delay:
            self.log("CLOSE!!!")
            self.close()

        if len(self.datas[0].close) < 1:
            return

        print(self.order)
        if self.order is not None:
            return

        # Check if we are in the market
        if self.p.order == "B":
            # BUY, BUY, BUY!!! (with default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy()
        elif self.p.order == "S":
            self.log('SELL CREATE, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.sell()

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
