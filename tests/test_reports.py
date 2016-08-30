# Note: It appears that for tickers to work that you have to register
# them only when the transaction connection is ready

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


@sp.ffi.callback("ApiTickerUpdateAddr")
def ticker_action(data):
    print("Ticker")
    print(sp.cdata_to_py(data[0]))


@sp.ffi.callback("ConnectedReplyAddr")
def connected_reply_func(host_type, con_status):
    print("connected", host_type, con_status)
    if host_type == 83 and con_status == 2:
        print(sp.get_all_orders())
        print(sp.get_all_trades())


@sp.ffi.callback("ApiPriceUpdateAddr")
def api_price_update_func(data):
    print("api_price_update")
    print(sp.cdata_to_py(data[0]))


@sp.ffi.callback("LoginReplyAddr")
def login_actions(ret_code, ret_msg):
    print("login")
    print(login['user_id'].encode("utf-8"))


sp.register_login_reply(login_actions)
sp.register_connecting_reply(connected_reply_func)
print(sp.login())
input("Press any key to exit")
sp.logout()
