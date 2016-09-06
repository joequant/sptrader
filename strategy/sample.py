import matplotlib
matplotlib.use('Agg', warn=False, force=True)
print(matplotlib.get_backend())
import backtrader as bt
import matplotlib.pyplot as plt
from backtrader.plot.plot import Plot

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from multiprocessing import Process
# Create a Strategy

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
sys.path.insert(0, os.path.join(location, "../sptrader"))
from spcsv import SharpPointCSVData
from spbroker import SharpPointBroker

class TestStrategy(bt.Strategy):
    params = (
        ('exitbars', 3),
        ('maperiod', 10)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime()
        print('%s, %s' % (dt.isoformat(' '), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
        
    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
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

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:
                    # current close less than previous close

                    if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy()

        else:
            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

def run_strategy(fname, kwargs):
    retval = ""
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    cerebro.setbroker(SharpPointBroker())

    # Create a Data Feed
    data = SharpPointCSVData(
        dataname=fname,
        product='HSIZ6',
        **kwargs)

    # Add the Data Feed to Cerebro
    cerebro.resampledata(data,
                         timeframe=bt.TimeFrame.Minutes,
                         compression=5)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    retval = retval + \
             ('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()
    plotter = Plot(style='candle')
    cerebro.plot(plotter)
    imgdata = open('out.svg', 'wb')
    plt.savefig(imgdata, format='svg')
    imgdata.close()
    # Print out the final result
    retval = retval + \
             ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    return retval

if __name__ == '__main__':
    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.realpath(__file__))
    datapath = os.path.join(modpath, '../data/ticker.txt')
    p = Process(target=run_strategy, args=(datapath, {"newdata": True,
                                                      "keepalive": True,
                                                      "debug" : True}))
    p.start()
    p.join()

