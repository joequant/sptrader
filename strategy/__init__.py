import sys
import os
import io
import base64
import matplotlib
matplotlib.use('Agg', warn=False, force=True)
import backtrader as bt
import matplotlib.pyplot as plt
from backtrader.plot.plot import Plot
from multiprocessing import Process, Queue

# must import first to initialize metaclass
from spfeed import SharpPointCSVData
from spbroker import SharpPointBroker
from spbacktester import SharpPointBackTester
import spstore
import strategy.strategylist
import datetime
from pytz import timezone
import traceback


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def run_strategy(name, kwargs, q):
    f = None
    try:
        if kwargs.get('dataname', None) is None or \
               kwargs['dataname'] == '':
            raise ValueError('missing dataname')
        modpath = os.path.dirname(os.path.realpath(__file__))
        logpath = os.path.join(modpath, '../data/log-%s-%s.txt' %
                               (kwargs['strategy'],
                                str(kwargs['id'])))
        f = open(logpath, "a")
        old_sysout = sys.stdout
        sys.stdout = Unbuffered(f)

        module = strategylist.dispatch[name]
        cerebro = bt.Cerebro()
        cerebro.addstrategy(module)
        store = spstore.SharpPointStore()
        broker = store.getbroker(backtest=kwargs.get('backtest', False))
        cerebro.setbroker(broker)

        # Create a Data Feed
        data = store.getdata(**kwargs)
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
        sys.stdout = old_sysout
        f.close()
        q.put((kwargs['strategy'], kwargs['id'], "done", ""))
        return None
    except:
        if f is not None:
            print(traceback.format_exc())
            sys.stdout = old_sysout
            f.close()
        print(traceback.format_exc())
        q.put((kwargs['strategy'], kwargs['id'], "error",
               repr(sys.exc_info())))
        raise


def parse_date(s):
    [d, t] = s.split()
    l = [int(x) for x in d.split('-')] + [int(x) for x in t.split(':')]
    return datetime.datetime(*l)


def run_backtest(kwargs):
    if kwargs.get('dataname', None) is None or \
           kwargs['dataname'] == '':
        raise ValueError('missing dataname')
    module = strategy.strategylist.dispatch[kwargs['strategy']]
    f = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = f
    cerebro = bt.Cerebro()
    cerebro.addstrategy(module)
    store = spstore.SharpPointStore()
    broker = store.getbroker(backtest=kwargs.get('backtest', True))
    cerebro.setbroker(broker)

    if kwargs.get('backtest_start_time', '').strip() != '':
        kwargs['fromdate'] = parse_date(kwargs['backtest_start_time'])

    if kwargs.get('backtest_end_time', '').strip() != '':
        kwargs['todate'] = parse_date(kwargs['backtest_end_time'])

    # Create a Data Feed
    data = store.getdata(
        **kwargs)
    data2 = bt.DataClone(dataname=data)
    data2.addfilter(bt.ReplayerMinutes, compression=5)
    cerebro.adddata(data)
    cerebro.adddata(data2)

    # Set the commission - 0.1% ... divide by 100 to remove the %
    initial_cash = kwargs.get("initial_cash", None)
    if initial_cash is not None:
        cerebro.broker.setcash(float(initial_cash))
#    cerebro.broker.setcommission(commission=0.0)

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


def run(name, id, kwargs):
    q = Queue()
    modpath = os.path.dirname(os.path.realpath(__file__))
    datapath = os.path.join(modpath, '../data/ticker-%s.txt')
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
    datapath = os.path.join(modpath, '../data/ticker-%s.txt')
    open(datapath, 'a').close()
    kwargs['tickersource'] = datapath
    kwargs['newdata'] = False
    kwargs['keepalive'] = False
    kwargs['debug'] = False
    kwargs['streaming'] = False
    try:
        return run_backtest(kwargs)
    except:
        return "<pre>" + traceback.format_exc() + "</pre>"


def strategy_list():
    return list(strategy.strategylist.dispatch.keys())


def params(name):
    return strategy.strategylist.dispatch[name].params._getpairs()


def headers(name):
    headers = strategy.strategylist.dispatch[name].headers()
    defaultData = params(name)
    for i in range(len(headers)):
        if 'defaultData' not in headers[i] and \
               headers[i]['field'] in defaultData:
            headers[i]['defaultData'] = defaultData[headers[i]['field']]
    return headers


class TimeFilter(object):
    def __init__(self, a, b):
        self.start_time = self.string_to_seconds(a)
        self.end_time = self.string_to_seconds(b)

    @staticmethod
    def string_to_seconds(s):
        v = s.split(":")
        r = int(v[0]) * 3600 + int(v[1]) * 60
        if len(v) > 2:
            r = r + int(v[2])
        return r

    @staticmethod
    def seconds_from_midnight(d):
        return (d - d.replace(hour=0, minute=0,
                              second=0, microsecond=0)).total_seconds()

    def intervals(self, a):
        ticktime_seconds = self.seconds_from_midnight(a)
        return (ticktime_seconds, self.start_time, self.end_time)

    def filter(self, a):
        ticktime_seconds = self.seconds_from_midnight(a)
        return (ticktime_seconds >= self.start_time and
                ticktime_seconds <= self.end_time)

if __name__ == '__main__':
    print(params('sample'))
    print(params('sample').get('exitbars', None))
    print(TimeFilter.string_to_seconds("14:30"))
    run("sample", 1, {'exitbars': 1})
