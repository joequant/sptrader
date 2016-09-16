import cffi
import os
import sys
import time
import threading
import backtrader as bt
import getpass

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
sys.path.insert(0, os.path.join(location, "..", "sptrader"))

import config
import cffi_to_py
import spbroker
import spcsv

cv = threading.Condition()
login = config.logininfo
passwd = getpass.getpass()
login['password'] = passwd
spbroker = spbroker.SharpPointBroker(login=login)
cerebro = bt.Cerebro()
data = spcsv.SharpPointCSVData(dataname=os.path.join(location, "../data/ticker.txt"),
                               product = "HSIZ6",
                               newdata=True)
cerebro.adddata(data)
cerebro.run()
spbroker.start()
input("Wait to buy")
spbroker.buy(None, data, 5, price=23500.0)
input("Press any key to logout")

