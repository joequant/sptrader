"""Base class for spstrategy classes"""

import sys  # To find out the script name (in argv[0])
import logging
import backtrader as bt

# Create a Strategy

class SharpPointStrategy(bt.Strategy):
    params = (
        ('log', sys.stdout),
        ('loglevel', logging.INFO)
    )

    @classmethod
    def headers(cls):
        return [
            {'headerName': "Loglevel",
             'field': "loglevel"},
            ]

    def log(self, *args, dt=None, level=logging.INFO):
        ''' Logging function fot this strategy'''
        if level < self.p.loglevel:
            return
        dt = dt or self.datas[0].datetime.datetime()
        print('%s, ' % dt.isoformat(' '), *args,
              file=self.p.log)

    def __init__(self):
        super().__init__()

    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Rejected]:
            self.log("REJECTED")
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))


    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        raise NotImplementedError
