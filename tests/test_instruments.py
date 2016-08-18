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
sp = sptrader.SPTrader()
sp.set_login_info(login['host'],
                  8080,
                  login['license'],
                  login['app_id'],
                  login['user_id'],
                  "test1")

@sp.ffi.callback("ApiTickerUpdateAddr")
def ticker_action(data):
    print("Ticker")

@sp.ffi.callback("ConnectedReplyAddr")
def connected_reply_func(host_type, con_status):
    print("connected", host_type, con_status)

@sp.ffi.callback("AccountInfoPushAddr")
def account_info_func(data):
    print("Account")
    print(data[0].NAV)
    print(sp.ffi.string(data[0].ClientId))
    print(data[0].CreditLimit)
    print(sp.ffi.string(data[0].MarginClass))

@sp.ffi.callback("LoginReplyAddr")
def login_actions(ret_code, ret_msg):
    print("login")
    print(login['user_id'].encode("utf-8"))
    user = sp.ffi.new("char[]", login['user_id'].encode("utf-8"))
    print(user)

    print(sp.api.SPAPI_GetAccBalCount(user))
    print(sp.get_login_status(80))
    print(sp.get_login_status(81))
    print(sp.get_login_status(83))
    print(sp.get_login_status(88))
    sp.api.SPAPI_RegisterTickerUpdate(ticker_action)
    print(sp.api.SPAPI_SubscribeTicker(
        user,
        b"003888", 1))
    print(sp.api.SPAPI_LoadInstrumentList());
    print(sp.api.SPAPI_GetInstrumentCount());
    print(sp.api.SPAPI_GetProductCount());


sp.api.SPAPI_RegisterAccountInfoPush(account_info_func)
sp.api.SPAPI_RegisterConnectingReply(connected_reply_func)
print(sp.login(login_actions))
input("Press any key to exit")
sp.logout()


