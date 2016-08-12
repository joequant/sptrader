import cffi
import os
import sys
import time
import threading
from ctypes import *

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
import sptrader
cv = threading.Condition()
sptrader = sptrader.SPTrader("demo.spsystem.info", 8080,
                             "57ABC58F6555F",
                             "SPDEMO",
                             "DEMO201608054",
                             "test1")


@sptrader.ffi.callback("LoginReplyAddr")
def login_actions(ret_code, ret_msg):
    cv.acquire()
    print("login")
    print(sptrader.get_login_status(81))
    print(sptrader.logout())
    input("Press any key to exit")
    cv.notify()
    cv.release()

cv.acquire()
print(sptrader.login(login_actions))
cv.wait()
cv.release()
