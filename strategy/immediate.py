"""Implements ImmediateStrategy"""
import spstrategy
# Create a Strategy


class ImmediateStrategy(spstrategy.SharpPointStrategy):
    """Immediate strategy automatically executes an order"""
    params = (
        ('qty', 1),
        ('delay', 5),
        ('cancel', 0),
        ('order', "B")
    )

    headers = [
        {'headerName': "Order",
         'field': "order"},
        {'headerName': "Cancel",
         'field': "cancel"},
        {'headerName': "Delay",
         'field': "delay"}
        ]

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
            if (self.p.cancel > 0):
                self.cancel(self.order)
            self.order = None

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

    def notify_order(self, order):
        super().notify_order(order)
        self.log("order notified", order)

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
