import backtrader as bt
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
# Create a Strategy

class ImmediateStrategy(bt.Strategy):
    params = (
        ('qty', 1),
        ('delay', 5),
        ('order', "B"),
        ('log', sys.stdout)
    )

    @classmethod
    def headers(cls):
        return [
            {'headerName': "Order",
             'field': "order"},
            {'headerName': "Delay",
             'field': "delay"}
            ]
    def log(self, *args, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime()
        print('%s, ' % dt.isoformat(' '), *args, file=self.p.log)

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
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
        self.log('%.2f %.2f' % (self.datas[0].open[0],
                                self.datas[1].open[0]))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if len(self.datas[0].close) > self.p.delay:
            self.close()
            self.order = None

        if len(self.datas[0].close) < 1:
            return

        if self.order:
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



