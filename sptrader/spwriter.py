import backtrader as bt
import itertools

class SharpPointWriter(bt.WriterFile):
    params = (
        ('csvsep', '; '),
        )
    def __init__(self, *args, **kwargs):
        super(SharpPointWriter, self).__init__(*args, **kwargs)
    def start(self):
        pass
    def writedict(self, dct, level=0, recurse=False):
        pass
    def writeiterable(self, iterable, func=None, counter=''):
        if self.p.csv_counter:
            iterable = itertools.chain([counter], iterable)

        if func is not None:
            iterable = map(lambda x: func(x), iterable)
        items = list(iterable)[3:9]
        items[0] = items[0].replace(" ", "/")
        items[0] = items[0].replace(":", "/").replace("-", "/")
        line = self.p.csvsep.join(items)
        self.writeline(line)
