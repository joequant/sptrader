import cffi
import os
import sys

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
import sptrader
sptrader = sptrader.SPTrader("demo.spsystem.info", 8080,
                             "DLLAPITEST",
                             "DLLAPITEST",
                             "SPAPI47",
                             "12345678")
print(sptrader.login())
print(sptrader.get_login_status(81))
print(sptrader.logout())
input("Press any key to exit")

