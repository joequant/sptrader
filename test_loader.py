import cffi
import os
import sys
import time
from ctypes import *

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
import sptrader
sptrader = sptrader.SPTrader("demo.spsystem.info", 8080,
                             "57ABC58F6555F",
                             "SPDEMO",
                             "DEMO201608054",
                             "test1")


LOGIN_FUNC = WINFUNCTYPE(None, c_long, c_char_p)
def login_actions(ret_code, ret_msg):
    print("login")
    print(sptrader.get_login_status(81))
    print(sptrader.logout())
login_func = LOGIN_FUNC(login_actions)
    
print(sptrader.login(login_func))

input("Press any key to exit")
