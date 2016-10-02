import spstore
from backtrader.metabase import MetaParams
from backtrader.utils.py3 import with_metaclass
from backtrader.brokers.bbroker import BackBroker

class MetaSharpPointBackTester(MetaParams):
    def __init__(cls, name, bases, dct):
        '''Class has already been created ... register'''
        # Initialize the class
        spstore.SharpPointStore.BackTestCls = cls


class SharpPointBackTester(with_metaclass(MetaSharpPointBackTester,
                                          BackBroker)):
    params = ()
    def init(self):
        super(SharpPointBackTester, self).init()


