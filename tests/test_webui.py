from flask import Flask, Response, jsonify, request, abort


import os
import sys
import cffi

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(location, "..", "sptrader"))

import config
from queue import Queue
from sse import ServerSentEvent
import sptrader

sp = sptrader.SPTrader()
subscriptions = []
app = Flask(__name__,
            static_url_path="/static",
            static_folder=os.path.join(location, "..",
                                                 "static"))


@app.route("/")
def hello():
    return app.send_static_file("sptrader.html")


@app.route("/logininfo")
def logininfo():
    return jsonify(config.logininfo)


@sp.ffi.callback("LoginReplyAddr")
def login_reply(ret_code, ret_msg):
    if ret_code == 0:
        ret_msg = ''
    else:
        ret_msg = sp.ffi.string(ret_msg).decode('utf-8')

    msg = {
        "id": "LoginReply",
        "ret_code": ret_code,
        "ret_msg": ret_msg
        }
    for sub in subscriptions[:]:
        sub.put(msg)
sp.register_login_reply(login_reply)


@sp.ffi.callback("ConnectedReplyAddr")
def connected_reply(host_type, con_status):
    msg = {
        "id": "ConnectedReply",
        "host_type": host_type,
        "con_status": con_status
        }
    for sub in subscriptions[:]:
        sub.put(msg)
sp.register_connecting_reply(connected_reply)


def send_data(id, data):
    msg = sp.cdata_to_dict(data[0])
    msg["id"] = id
    for sub in subscriptions[:]:
        sub.put(msg)


@sp.ffi.callback("AccountInfoPushAddr")
def account_info_push(data):
    send_data("AccountInfoPush", data)
sp.register_account_info_push(account_info_push)


@sp.ffi.callback("AccountPositionPushAddr")
def account_position_push(data):
    send_data("AccountPositionPush", data)
sp.register_account_position_push(account_position_push)


@sp.ffi.callback("ApiTradeReportAddr")
def trade_report(data):
    send_data("ApiTradeReport", data)
sp.register_trade_report(trade_report)


@sp.ffi.callback("ApiPriceUpdateAddr")
def api_price_update(data):
    send_data("ApiPriceUpdate", data)
sp.register_api_price_update(api_price_update)


@sp.ffi.callback("ApiTickerUpdateAddr")
def ticker_update(data):
    send_data("ApiTickerUpdate", data)
sp.register_ticker_update(ticker_update)


@sp.ffi.callback("InstrumentListReplyAddr")
def instrument_list_reply(is_ready, ret_msg):
    data = {"is_ready": is_ready,
            "ret_msg": ret_msg,
            "data": sp.get_instrument()}
    send_data("InstrumentListReply", data)


@sp.ffi.callback("ProductListByCodeReplyAddr")
def product_list_by_code(inst_code, is_ready, ret_msg):
    data = {
        "inst_code": inst_code,
        "is_ready": is_ready,
        "ret_msg": ret_msg,
        "data": sp.get_product()}
    send_data("ProductListByCode", data)
sp.register_product_list_by_code_reply(product_list_by_code)


@app.route("/login", methods=['POST'])
def login():
    global sp
    if not request.json:
        abort(400)
    sp.set_login_info(request.json["host"],
                      request.json["port"],
                      request.json["license"],
                      request.json["app_id"],
                      request.json["user_id"],
                      request.json["password"])
    return jsonify({"retval": sp.login()})


@app.route("/get-login-status/<int:host_id>")
def get_login_status(host_id):
    global sp
    if host_id not in [80, 81, 83, 87, 88]:
        return "-1"
    return "%d" % sp.get_login_status(host_id)


@app.route("/ping")
def ping():
    msg = {
        "id": "ping",
        "msg": "Ping"
        }
    for sub in subscriptions[:]:
        sub.put(msg)
    return "OK"


@app.route("/logout")
def logout():
    global sp
    sp.logout()
    return "OK"


@app.route("/subscribe-ticker/<string:product>")
def subscribe_ticker(product):
    sp.subscribe_ticker(product, 1)


@app.route("/unsubscribe-ticker/<string:product>")
def unsubscribe_ticker(product):
    sp.subscribe_ticker(product, 0)


@app.route("/subscribe-price/<string:product>")
def subscribe_price(product):
    sp.subscribe_price(product, 1)


@app.route("/unsubscribe-price/<string:product>")
def unsubscribe_price(product):
    sp.unsubscribe_price(product, 0)


@app.route("/get-account-info")
def get_account_info():
    sp.get_acc_bal_count()


@app.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                id = result['id']
                ev = ServerSentEvent(result, id)
                yield ev.encode()
        except GeneratorExit:  # Or maybe use flask signals
            subscriptions.remove(q)
    return Response(gen(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True)
