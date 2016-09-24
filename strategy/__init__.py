import matplotlib
matplotlib.use('Agg', warn=False, force=True)
import backtrader as bt
import matplotlib.pyplot as plt
from backtrader.plot.plot import Plot
import sys
import os
import multiprocessing
from spfeed import SharpPointCSVData
from spbroker import SharpPointBroker
import spstore
import strategy.strategylist

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def run_strategy(module, fname, kwargs):
    modpath = os.path.dirname(os.path.realpath(__file__))
    logpath = os.path.join(modpath, '../data/log-%s-%s.txt' % \
                           (kwargs['strategy'],
                            str(kwargs['id'])))
    f = open(logpath, "w")
    sys.stdout = Unbuffered(f)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(module)
    store = spstore.SharpPointStore()
    broker = store.getbroker(backtest=kwargs.get('backtest', False))
    cerebro.setbroker(broker)

    # Create a Data Feed
    data = store.getdata(
        dataname=fname,
        **kwargs)
    data2 = bt.DataClone(dataname=data)
    data2.addfilter(bt.ReplayerMinutes, compression=5)
    cerebro.adddata(data)
    cerebro.adddata(data2)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()
    plotter = Plot(style='candle')
    cerebro.plot(plotter)
    imgdata = open('out.svg', 'wb')
    plt.savefig(imgdata, format='svg')
    imgdata.close()
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    f.close()
    return None

def run(name, id, kwargs):
    module = strategylist.dispatch[name]
    modpath = os.path.dirname(os.path.realpath(__file__))
    datapath = os.path.join(modpath, '../data/ticker.txt')
    kwargs['newdata'] = True
    kwargs['keepalive'] = True
    kwargs['debug'] = True
    kwargs['streaming'] = True
    p = multiprocessing.Process(target=run_strategy,
                                args=(module, datapath, kwargs))
    return p

def params(name):
    return strategylist.dispatch[name].params._getitems()

if __name__ == '__main__':
    print(params('sample'))
    run("sample", 1, {'exitbars':1})
