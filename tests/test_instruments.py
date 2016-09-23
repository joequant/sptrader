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


@sp.ffi.callback("AccountInfoPushAddr")
def account_info_func(data):
    print("Account")
    print(sp.cdata_to_py(data[0]))
    print(sp.fields(data[0]))

@sp.ffi.callback("InstrumentListReplyAddr")
def instrument_list_reply_func(is_ready, ret_msg):
    print("InstrumentListReply")
    print(is_ready)
    print(sp.cdata_to_py(ret_msg))
    print(sp.get_instrument_count())


@sp.ffi.callback("ApiPriceUpdateAddr")
def api_price_update_func(data):
    print("api_price_update")
    print(sp.cdata_to_py(data[0]))


@sp.ffi.callback("LoginReplyAddr")
def login_actions(ret_code, ret_msg):
    print("login")
    print(login['user_id'])
    print("instrument_list", sp.load_instrument_list())
    print("price", sp.get_price_by_code("HSIQ6"))
    print(sp.get_acc_bal_count())
    print(sp.subscribe_price("HSIQ6", 1))
    print(sp.subscribe_ticker("HSIQ6", 1))
    print(sp.get_instrument_count())
    print(sp.get_product_count())

sp.register_login_reply(login_actions)
sp.register_account_info_push(account_info_func)
sp.register_connecting_reply(connected_reply_func)
sp.register_instrument_list_reply(instrument_list_reply_func)
sp.register_price_update(api_price_update_func)
sp.register_ticker_update(ticker_action)
print(sp.login())

input("Press any key to exit")
sp.logout()
