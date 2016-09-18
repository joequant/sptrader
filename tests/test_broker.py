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
import spstore
import spfeed
import spbroker

cv = threading.Condition()

cerebro = bt.Cerebro()
store = spstore.SharpPointStore()
broker = store.getbroker()
data = store.getdata(dataname=os.path.join(location, "../data/ticker.txt"),
                     product = "HSIZ6",
                     newdata=True,
                     streaming=True)

if not store.isloggedin():
    login = config.logininfo
    passwd = getpass.getpass()
    login['password'] = passwd
    store.setlogin(login)

cerebro.adddata(data)
cerebro.run()
broker.start()
input("Wait to buy")
broker.buy(None, data, 5, price=23500.0)
input("Press any key to logout")

