import spstore
from backtrader.metabase import MetaParams
from backtrader.utils.py3 import with_metaclass
from backtrader.brokers.bbroker import BackBroker
from backtrader.comminfo import CommInfoBase

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
    def getcommissioninfo(self, data):
        if data._name in self.comminfo:
            return self.comminfo[data._name]
        if data._name[0:3] == 'HSI':
            self.setcommission(stocklike=False, mult=50.0,
                               name=data._name,
                               commtype=CommInfoBase.COMM_FIXED)
        elif data._name[0:3] == 'MHI':
            self.setcommission(stocklike=False, mult=10.0,
                               name=data._name,
                               commtype=CommInfoBase.COMM_FIXED)
        print(self.comminfo)
        return super(SharpPointBackTester, self).getcommissioninfo(data)
