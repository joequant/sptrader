import cffi
import os
import sys
import time
import threading

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
sys.path.insert(0, os.path.join(location, "..", "sptrader"))

import sptrader
import config
import cffi_to_py

cv = threading.Condition()
login = config.logininfo
sp = sptrader.SPTrader()

sp.set_login_info(login['host'],
                  8080,
                  login['license'],
                  login['app_id'],
                  login['user_id'],
                  "test1")


@sp.ffi.callback("LoginReplyAddr")
def login_actions(ret_code, ret_msg):
    print("login")
    print(login['user_id'])

sp.register_login_reply(login_actions)
print(sp.login())

input("Press any key to exit")
sp.logout()
