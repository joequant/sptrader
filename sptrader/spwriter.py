import backtrader as bt

class SharpPointWriter(bt.WriterFile):
    def __init__(self, *args, **kwargs):
        super(SharpPointWriter, self).__init__(*args, **kwargs)
