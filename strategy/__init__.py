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
import logging
import pprint
import copy
import inspect

# must import first to initialize metaclass
from spfeed import SharpPointCSVData
from spbroker import SharpPointBroker
from spbacktester import SharpPointBackTester
import spstore
import strategy.strategylist
import datetime
from pytz import timezone
import traceback
import jitter


def check_params(kwargs, slist):
    for s in slist:
        if kwargs.get(s, None) is None or \
               kwargs[s] == '':
            raise ValueError('missing %s' % str(s))


def run_strategy(kwargs, q):
    f = None
    try:
        check_params(kwargs, ['strategy', 'dataname', 'id'])
        modpath = os.path.dirname(os.path.realpath(__file__))
        logpath = os.path.join(modpath, '../data/log-%s.txt' %
                               (str(kwargs['id'])))
        f = open(logpath, "a", 1)
        stratargs = {}
        module = strategy.strategylist.dispatch[kwargs['strategy']]
        stratparams = module.params._getpairs()
        for k, v in kwargs.items():
            if k in stratparams:
                s = stratparams[k]
                if isinstance(s, int):
                    stratargs[k] = int(v)
                elif isinstance(s, float):
                    stratargs[k] = float(v)
                else:
                    stratargs[k] = v
        stratargs['log'] = f
        stratargs['strategy'] = module
        cerebro = bt.Cerebro()
        cerebro.addstrategy(**stratargs)
        store = spstore.SharpPointStore(log=f)
        broker = store.getbroker()
        cerebro.setbroker(broker)

        # Create a Data Feed
        data = store.getdata(**kwargs)
        data2 = bt.DataClone(dataname=data)
        data2.addfilter(bt.ReplayerMinutes, compression=5)
        cerebro.adddata(data)
        cerebro.adddata(data2)

        # Print out the starting conditions
        print('Starting strategy "{}" at "{}"'.format(kwargs['strategy'],
                                                      datetime.datetime.now()),
              file=f)
        print('Using module file "{}"'.format(inspect.getsourcefile(module)),
              file=f)
        print('{}'.format(pprint.pformat(kwargs)), file=f)
        # Run over everything
        cerebro.run()
        # Print out the final result
        print('Finishing strategy "{}" at "{}"'.format(kwargs['strategy'],
                                                       datetime.datetime.now()),
              file=f)
        f.close()
        q.put((kwargs['strategy'], kwargs['id'], "done", ""))
        return None
    except:
        if f is not None:
            print(traceback.format_exc(), file=f)
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
    check_params(kwargs, ['strategy', 'dataname'])
    stratargs = {}
    f = io.StringIO()
    module = strategy.strategylist.dispatch[kwargs['strategy']]
    stratparams = module.params._getpairs()
    for k, v in kwargs.items():
        if k in stratparams:
            s = stratparams[k]
            if isinstance(s, int):
                stratargs[k] = int(v)
            elif isinstance(s, float):
                stratargs[k] = float(v)
            else:
                stratargs[k] = v
    stratargs['log'] = f
    stratargs['strategy'] = module
    cerebro = bt.Cerebro()
    cerebro.addstrategy(**stratargs)
    store = spstore.SharpPointStore(log=f)
    broker = store.getbroker(backtest=kwargs.get('backtest', True))
    cerebro.setbroker(broker)

    feedargs = copy.copy(kwargs)
    if kwargs.get('backtest_start_time', '').strip() != '':
        feedargs['fromdate'] = parse_date(kwargs['backtest_start_time'])

    if kwargs.get('backtest_end_time', '').strip() != '':
        feedargs['todate'] = parse_date(kwargs['backtest_end_time'])

    # Create a Data Feed
    data = store.getdata(**feedargs)
    if float(kwargs['jitter']) >= 0.0:
        data.addfilter(jitter.JitterFilter,
                       jitter=float(kwargs['jitter']))
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

    print('Starting strategy "{}" at "{}"'.format(kwargs['strategy'],
                                                  datetime.datetime.now()),
          file=f)
    print('Using module file "{}"'.format(inspect.getsourcefile(module)),
          file=f)
    print('{}'.format(pprint.pformat(kwargs)), file=f)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue(), file=f)

    # Run over everything
    cerebro.run()
    imgdata = io.BytesIO()
    plot_type = kwargs.get("plot", "candle")
    if plot_type != "none":
        plotter = Plot(style='candle', bardownfill=False)
        cerebro.plot(plotter)
        plt.savefig(imgdata, format='svg')

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue(),
          file=f)
    print('Finishing strategy "{}" at "{}"'.format(kwargs['strategy'],
                                                   datetime.datetime.now()),
          file=f)
    retval = """
<html>
<head>
<title>Backtest - {}</title>
</head>
<body>
""".format(kwargs['id'])
    if plot_type != "none": 
        retval += '<img src="data:image/svg+xml;base64,%s" /><br>' % \
             base64.b64encode(imgdata.getvalue()).decode('ascii')
    retval += '<pre>%s</pre></body></html>' % f.getvalue()
    imgdata.close()
    plt.close('all')
    f.close()
    return retval


def run(kwargs):
    q = Queue()
    kwargs['newdata'] = True
    kwargs['keepalive'] = True
    if 'loglevel' not in kwargs:
        kwargs['loglevel'] = logging.WARNING
    kwargs['streaming'] = True
    if 'tickersource' not in kwargs:
        kwargs['tickersource'] = "ticker-%{instrument}.txt"
    p = Process(target=run_strategy,
                args=(kwargs, q))
    p.daemon = True
    p.start()
    return (p, q)


def backtest(kwargs):
    kwargs['newdata'] = False
    kwargs['keepalive'] = False
    if 'loglevel' not in kwargs:
        kwargs['loglevel'] = logging.WARNING
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
    my_headers = strategy.strategylist.dispatch[name].header_list()
    defaultData = params(name)
    for header in my_headers:
        if 'defaultData' not in header and \
               header['field'] in defaultData:
            header['defaultData'] = defaultData[header['field']]
    return my_headers


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
