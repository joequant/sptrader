#!/usr/bin/python3
import os
import sys
location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
sys.path.insert(0, os.path.join(location, ".."))
sys.path.insert(0, os.path.join(location, "..", "sptrader"))

import strategy
print(strategy.backtest({"dataname": "HSIZ6",
                        "tickersource": "ticker-%{instrument}.txt", 
                         "initial_cash": 100000.00,
                         "strategy" : "sample"}))
