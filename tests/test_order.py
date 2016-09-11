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


@sp.ffi.callback("ConnectedReplyAddr")
def connected_reply_func(host_type, con_status):
    print("connected", host_type, con_status)


@sp.ffi.callback("ApiOrderReportAddr")
def api_order_report(rec_no, order):
    print("register order %d" % rec_no)
    print(sp.cdata_to_py(order[0]))


@sp.ffi.callback("ApiOrderRequestFailedAddr")
def api_order_request_failed(action,
                             order,
                             err_code,
                             err_msg):
    d = sp.cdata_to_py(order)
    d['action'] = action
    d['err_code'] = err_code
    d['err_msg'] = err_msg
    print(d)


@sp.ffi.callback("ApiTradeReportAddr")
def api_order_request_failed(rec_no, trade):
    d = sp.cdata_to_py(trade)
    d['rec_no'] = rec_no
    print(d)


@sp.ffi.callback("ApiOrderBeforeSendReportAddr")
def api_order_before_send_report(order):
    d = sp.cdata_to_py(order[0])
    print(d)


@sp.ffi.callback("LoginReplyAddr")
def login_actions(ret_code, ret_msg):
    print("login")
    print(login['user_id'])

sp.register_connecting_reply(connected_reply_func)
sp.register_order_report(api_order_report)
sp.register_order_before_send_report(api_order_before_send_report)
sp.register_login_reply(login_actions)

print(sp.login())
input("Press any key to exit")
d = {"BuySell": "B",
     "Qty": 1,
     "ProdCode": "HSIZ6",
     "DecInPrice": 0,
     "Ref": "test",
     "Ref2": "",
     "ClOrderId": "test2",
     "OpenClose": 0,
     "CondType": 0,
     "OrderType": 0,
     "ValidType": 0,
     "StopType": 0,
     "OrderOptions": 0,
     "Price": 24000.0 }
print(d)
print("result: ", sp.order_add(d))
input("Press any key to logout")
sp.logout()
