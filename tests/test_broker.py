import cffi
import os
import sys
import time
import threading
import backtrader as bt

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
sys.path.insert(0, os.path.join(location, "..", "sptrader"))

import config
import cffi_to_py
import spbroker
import spcsv

cv = threading.Condition()
login = config.logininfo
spbroker = spbroker.SharpPointBroker()

d = {"BuySell": "B",
     "Qty": 1,
     "ProdCode": "HSIZ6",
     "DecInPrice": 0,
     "Ref": "test",
     "Ref2": "",
     "ClOrderId": "test2",
     "OpenClose": 0,
     "CondType": 0,
     "OrderType": 0,
     "ValidType": 0,
     "StopType": 0,
     "OrderOptions": 0,
     "Price": 24000.0 }
print(d)
cerebro = bt.Cerebro()
data = spcsv.SharpPointCSVData(dataname=os.path.join(location, "../data/ticker.txt"),
                         product = "HSIZ6")
cerebro.adddata(data)
cerebro.run()
spbroker.start()
spbroker.buy(None, data, 5, price=23500.0)
input("Press any key to logout")

