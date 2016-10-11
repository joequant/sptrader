import sys  # To find out the script name (in argv[0])
import logging
import spstrategy
import backtrader as bt
# Create a Strategy

class SampleStrategy(spstrategy.SharpPointStrategy):
    params = (
        ('exitbars', 3),
        ('maperiod', 10),
    )

    headers =  [
        {'headerName': "Exitbars",
         'field': "exitbars"},
        {'headerName': "Maperiod",
         'field': "maperiod"}
        ]

    def __init__(self):
        super().__init__()
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[1].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
        
    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f %.2f' % (self.dataclose[0],self.datas[1].close[0]))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        if len(self.dataclose) < 3:
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




