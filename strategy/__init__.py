import matplotlib
matplotlib.use('Agg', warn=False, force=True)
import backtrader as bt
import matplotlib.pyplot as plt
from backtrader.plot.plot import Plot
import sys
import os
import io
import base64
from multiprocessing import Process, Queue
from spfeed import SharpPointCSVData
from spbroker import SharpPointBroker
import spstore
import strategy.strategylist
from datetime import datetime
from pytz import timezone

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def run_strategy(name, kwargs, q):
    try:
        if kwargs.get('dataname', None) is None or \
               kwargs['dataname'] == '':
            raise ValueError('missing dataname')
        module = strategylist.dispatch[name]
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
            **kwargs)
        data2 = bt.DataClone(dataname=data)
        data2.addfilter(bt.ReplayerMinutes, compression=5)
        cerebro.adddata(data)
        cerebro.adddata(data2)

        # Print out the starting conditions
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
        # Run over everything
        cerebro.run()
        # Print out the final result
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        f.close()
        q.put((kwargs['strategy'], kwargs['id'], "done", ""))
        return None
    except:
        q.put((kwargs['strategy'], kwargs['id'], "error",
               repr(sys.exc_info())))
        raise

def run_backtest(kwargs):
    try:
        if kwargs.get('dataname', None) is None or \
               kwargs['dataname'] == '':
            raise ValueError('missing dataname')
        module = strategylist.dispatch[kwargs['strategy']]
        modpath = os.path.dirname(os.path.realpath(__file__))
        f = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = f
        cerebro = bt.Cerebro()
        cerebro.addstrategy(module)
        store = spstore.SharpPointStore()
        broker = store.getbroker(backtest=kwargs.get('backtest', True))
        cerebro.setbroker(broker)
        
        # Create a Data Feed
        data = store.getdata(
            **kwargs)
        data2 = bt.DataClone(dataname=data)
        data2.addfilter(bt.ReplayerMinutes, compression=5)
        cerebro.adddata(data)
        cerebro.adddata(data2)
        
        # Set the commission - 0.1% ... divide by 100 to remove the %
        cerebro.broker.setcommission(commission=0.0)

        # Print out the starting conditions
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
        # Run over everything
        cerebro.run()
        plotter = Plot(style='candle')
        cerebro.plot(plotter)
        imgdata = io.BytesIO() 
        plt.savefig(imgdata, format='svg')

        # Print out the final result
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        retval = '<img src="data:image/svg+xml;base64,%s" /><br>' % \
                 base64.b64encode(imgdata.getvalue()).decode('ascii') + \
                 '<pre>%s</pre>' % f.getvalue()
        imgdata.close()
        f.close()
        sys.stdout = old_stdout
        return retval
    except:
        return repr(sys.exc_info())

def run(name, id, kwargs):
    q = Queue()
    modpath = os.path.dirname(os.path.realpath(__file__))
    datapath = os.path.join(modpath, '../data/ticker.txt')
    open(datapath, 'a').close()
    kwargs['tickersource'] = datapath
    kwargs['newdata'] = True
    kwargs['keepalive'] = True
    kwargs['debug'] = True
    kwargs['streaming'] = True
    p = Process(target=run_strategy,
                args=(name, kwargs, q))
    p.daemon = True
    p.start()
    return (p, q)

def backtest(kwargs):
    modpath = os.path.dirname(os.path.realpath(__file__))
    datapath = os.path.join(modpath, '../data/ticker.txt')
    open(datapath, 'a').close()
    kwargs['tickersource'] = datapath
    kwargs['newdata'] = False
    kwargs['keepalive'] = False
    kwargs['debug'] = False
    kwargs['streaming'] = False
    return run_backtest(kwargs)

def strategy_list():
    return list(strategy.strategylist.dispatch.keys())

def params(name):
    return strategy.strategylist.dispatch[name].params._getpairs()

def headers(name):
    headers = strategy.strategylist.dispatch[name].headers()
    defaultData = params(name)
    for i in range(len(headers)):
        if not 'defaultData' in headers[i] and \
               headers[i]['field'] in defaultData:
            headers[i]['defaultData'] = defaultData[headers[i]['field']]
    return headers


def string_to_seconds(s):
    v = s.split(":")
    r = int(v[0]) * 3600 + int(v[1]) * 60
    if len(v) > 2:
        r = r + int(v[2])
    return r

def seconds_today(tz='UTC'):
    timez = timezone(tz)
    now = datetime.now(timez)
    return (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

if __name__ == '__main__':
    print(params('sample'))
    print(params('sample').get('exitbars', None))
    print(string_to_seconds("14:30"))
    print(seconds_today())
    print(seconds_today('Asia/Hong_Kong'))
    run("sample", 1, {'exitbars':1})

