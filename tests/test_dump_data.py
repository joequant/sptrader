#!/usr/bin/python3
import backtrader as bt
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Create a Stratey
location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
sys.path.insert(0, os.path.join(location, "../sptrader"))
from spfeed import SharpPointCSVData
from spbroker import SharpPointBroker
from spbacktester import SharpPointBackTester
import spstrategy
import spstore
import jitter

class DumpStrategy(spstrategy.SharpPointStrategy):
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log(bt.num2date(self.datas[0].datetime[0]),
                 bt.num2date(self.datas[1].datetime[0]),
                 self.datas[0].open[0],
                 self.datas[1].open[0])


def run_strategy():
    retval = ""

    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy=DumpStrategy)
    store = spstore.SharpPointStore(gateway=None)
    broker = store.getbroker(backtest=True)
    cerebro.setbroker(broker)
    
    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.realpath(__file__))
    datapath = os.path.join(modpath, '../data/HSI_20160902.txt')

    # Create a Data Feed
    data = SharpPointCSVData(
        dataname='HSIZ6',
        tickersource=datapath,
        newdata = False,
        keepalive = False,
        loglevel=0,
        streaming=False
        )
    data.addfilter(jitter.JitterFilter)
    data2 = bt.DataClone(dataname=data)
    data2.addfilter(bt.ReplayerMinutes, compression=5)
    cerebro.adddata(data)
    cerebro.adddata(data2)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    retval = retval + \
             ('Starting')

    # Run over everything
    cerebro.run()
    cerebro.plot(style='candle', bardownfill=False)
    # Print out the final result
    retval = retval + \
             ('Finishing')
    return retval

if __name__ == '__main__':
    print(run_strategy())
