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
log_subscriptions = []
tickers = []
ticker_products = set()
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
    for sub in log_subscriptions[:]:
        sub.put(msg)
sp.register_login_reply(login_reply)

def send_dict(id, msg):
    msg["id"] = id
    for sub in log_subscriptions[:]:
        sub.put(msg)


def send_cdata(id, data):
    send_dict(id, sp.cdata_to_py(data[0]))


@sp.ffi.callback("AccountInfoPushAddr")
def account_info_push(data):
    send_cdata("AccountInfoPush", data)
sp.register_account_info_push(account_info_push)


@sp.ffi.callback("AccountPositionPushAddr")
def account_position_push(data):
    send_cdata("AccountPositionPush", data)
sp.register_account_position_push(account_position_push)


@sp.ffi.callback("ApiTradeReportAddr")
def trade_report(rec_no, data):
    send_cdata("ApiTradeReport", data)
sp.register_trade_report(trade_report)


@sp.ffi.callback("ApiPriceUpdateAddr")
def api_price_update(data):
    send_cdata("ApiPriceUpdate", data)
sp.register_api_price_update(api_price_update)


@sp.ffi.callback("ApiTickerUpdateAddr")
def ticker_update(data):
    send_cdata("ApiTickerUpdate", data)
    for t in tickers[:]:
        t.put(sp.cdata_to_py(data[0]))
sp.register_ticker_update(ticker_update)


@sp.ffi.callback("InstrumentListReplyAddr")
def instrument_list_reply(is_ready, ret_msg):
    data = {"is_ready": is_ready,
            "ret_msg": ret_msg,
            "data": sp.get_instrument()}
    send_cdata("InstrumentListReply", data)


@sp.ffi.callback("ProductListByCodeReplyAddr")
def product_list_by_code(inst_code, is_ready, ret_msg):
    data = {
        "inst_code": inst_code,
        "is_ready": is_ready,
        "ret_msg": ret_msg,
        "data": sp.get_product()}
    send_cdata("ProductListByCode", data)
sp.register_product_list_by_code_reply(product_list_by_code)


@sp.ffi.callback("ConnectedReplyAddr")
def connected_reply(host_type, con_status):
    msg = {
        "id": "ConnectedReply",
        "host_type": host_type,
        "con_status": con_status
        }
    for sub in log_subscriptions[:]:
        sub.put(msg)
    if host_type == 83 and con_status == 2:
        sp.register_ticker_update(ticker_update)
        for p in ticker_products:
            sp.subscribe_ticker(p, 1)
sp.register_connecting_reply(connected_reply)


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


@app.route("/login-status/<int:host_id>")
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
    for sub in log_subscriptions[:]:
        sub.put(msg)
    return "OK"


@app.route("/logout")
def logout():
    global sp
    sp.logout()
    return "OK"


@app.route("/ticker/subscribe/<string:products>")
def subscribe_ticker(products):
    for p in products.split(","):
        ticker_products.add(p)
        if sp.ready() == 0:
            sp.subscribe_ticker(p, 1)
    if sp.ready() != 0:
        return "NOLOGIN"
    else:
        send_dict("UpdateTickers",
                  {"data": list(ticker_products)})
        return "OK"


@app.route("/ticker/unsubscribe/<string:products>")
def unsubscribe_ticker(products):
    for p in products.split(","):
        ticker_products.discard(p)
        if sp.ready() == 0:
            sp.subscribe_ticker(p, 0)
    if sp.ready() != 0:
        return "NOLOGIN"
    else:
        send_dict("UpdateTickers",
                  {"data": list(ticker_products)})
        return "OK"


@app.route("/ticker/list")
def list_ticker():
    return jsonify({"data": list(ticker_products)})


@app.route("/trade/list")
def list_trade():
    return jsonify({"data": sp.get_all_trades()})


@app.route("/order/list")
def list_order():
    return jsonify({"data": sp.get_all_orders()})


@app.route("/price/subscribe/<string:products>")
def subscribe_price(products):
    if sp.ready() != 0:
        return "NOT READY"
    for p in products.split(","):
        sp.subscribe_price(p, 1)
    return "OK"


@app.route("/price/unsubscribe/<string:products>")
def unsubscribe_price(products):
    if sp.ready() != 0:
        return "NOT READY"
    for p in products.split(","):
        sp.unsubscribe_price(p, 0)
    return "OK"


@app.route("/account-info")
def get_account_info():
    if sp.ready() != 0:
        return "NOT READY"
    sp.get_acc_bal_count()
    return "OK"


@app.route("/log/subscribe")
def subscribe():
    def gen():
        q = Queue()
        log_subscriptions.append(q)
        try:
            while True:
                result = q.get()
                id = result['id']
                ev = ServerSentEvent(result, id)
                yield ev.encode()
        except GeneratorExit:  # Or maybe use flask signals
            log_subscriptions.remove(q)
    return Response(gen(), mimetype="text/event-stream")


@app.route("/schema/<string:structure>")
def schema(structure):
    return jsonify({"retval": sp.fields(structure)})


@app.route("/ticker/get")
def ticker():
    def gen():
        q = Queue()
        tickers.append(q)
        try:
            while True:
                t = q.get()
                yield "%f,%d,%d,%d,%s,%s\n" % (t['Price'],
                                               t['Qty'],
                                               t['TickerTime'],
                                               t['DealSrc'],
                                               t['ProdCode'],
                                               t['DecInPrice'])
        except GeneratorExit:  # Or maybe use flask signals
            tickers.remove(q)
    return Response(gen(), mimetype="text/plain")


if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True)
