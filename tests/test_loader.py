import cffi
import os
import sys
import time
import threading
from ctypes import *

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
sys.path.insert(0, os.path.join(location, "..", "sptrader"))

import sptrader
import config
cv = threading.Condition()
login = config.logininfo;
sptrader = sptrader.SPTrader(login['host'],
                             login['port'],
                             login['license'],
                             login['app_id'],
                             login['user_id'],
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
