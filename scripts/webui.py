#!/usr/bin/python3
import os
import sys
import time
import threading
import json
import errno
import datetime
from queue import Queue

from flask import Flask, Response, jsonify, request, abort
location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(location, "..", "sptrader"))
sys.path.insert(0, os.path.join(location, ".."))
data_dir = os.path.join(location, "..", "data")

try:
    os.makedirs(data_dir)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

ticker_file = os.path.join(data_dir, "ticker-%s.txt")


def get_ticker(s):
    if "/" in s:
        raise ValueError
    return ticker_file % s

import config

from sse import ServerSentEvent
import sptrader
import strategy
import strategy.strategylist

sp = sptrader.SPTrader()
log_subscriptions = []
empty_cache = {"connected": {},
               "account_info": None}
info_cache = empty_cache
ticker_products = set()
app = Flask(__name__,
            static_url_path="/static",
            static_folder=os.path.join(location, "..",
                                       "static"))


@app.route("/")
def hello():
    return app.send_static_file("sptrader.html")


def send_dict(event_id, msg):
    for sub in log_subscriptions[:]:
        sub.put((event_id, msg))


def send_cdata(event_id, data):
    send_dict(event_id, {"data": sp.cdata_to_py(data[0])})


@app.route("/login-info")
def logininfo():
    d = {"info": config.logininfo,
         "status": "%d" % sp.get_login_status(80)}
    if info_cache['connected'] is not None:
        d['connected'] = info_cache['connected']
    if info_cache['account_info'] is not None:
        d['account_info'] = info_cache['account_info']
    d['account_fields'] = sp.fields("SPApiAccInfo")
    d['strategy_list'] = strategy.strategy_list()
    return jsonify(d)


@sp.ffi.callback("LoginReplyAddr")
def login_reply(ret_code, ret_msg):
    if ret_code == 0:
        ret_msg = ''
    else:
        ret_msg = sp.ffi.string(ret_msg).decode('utf-8')
    send_dict("LoginReply", {
        "ret_code": ret_code,
        "ret_msg": ret_msg
        })
sp.register_login_reply(login_reply)


@sp.ffi.callback("ConnectedReplyAddr")
def connected_reply(host_type, con_status):
    send_dict("ConnectedReply", {
        "host_type": host_type,
        "con_status": con_status
        })
    info_cache['connected'][host_type] = con_status
    if host_type == 83 and con_status == 2:
        sp.register_ticker_update(ticker_update)
        for p in ticker_products:
            sp.subscribe_ticker(p, 1)
sp.register_connecting_reply(connected_reply)


@sp.ffi.callback("ApiOrderRequestFailedAddr")
def order_request_failed(action, order, error_code, error_msg):
    send_dict("OrderRequestFailed", {
        "action": ord(action),
        "data": sp.cdata_to_py(order[0]),
        "error_code": error_code,
        "error_msg": sp.ffi.string(error_msg).decode('utf-8')})
sp.register_order_request_failed(order_request_failed)


@sp.ffi.callback("ApiOrderReportAddr")
def order_report(rec_no, data):
    send_dict("OrderReport", {
        "rec_no": rec_no,
        "data": sp.cdata_to_py(data[0])
        })
sp.register_order_report(order_report)


@sp.ffi.callback("ApiOrderBeforeSendReportAddr")
def api_order_before_send_report(data):
    send_cdata("OrderBeforeSendReport", data)
sp.register_order_before_send_report(api_order_before_send_report)


@sp.ffi.callback("AccountLoginReplyAddr")
def account_login_reply(accNo, ret_code, ret_msg):
    send_dict("AccountLoginReply", {
        "accNo": accNo,
        "ret_code": ret_code,
        "ret_msg": ret_msg
        })
sp.register_account_login_reply(account_login_reply)


@sp.ffi.callback("AccountLogoutReplyAddr")
def account_logout_reply(ret_code, ret_msg):
    send_dict("AccountLogoutReply", {
        "ret_code": ret_code,
        "ret_msg": ret_msg
        })
sp.register_account_logout_reply(account_logout_reply)


@sp.ffi.callback("AccountInfoPushAddr")
def account_info_push(data):
    info_cache['account_info'] = sp.cdata_to_py(data[0])
    send_cdata("AccountInfoPush", data)
sp.register_account_info_push(account_info_push)


@sp.ffi.callback("AccountPositionPushAddr")
def account_position_push(data):
    send_cdata("AccountPositionPush", data)
sp.register_account_position_push(account_position_push)


@sp.ffi.callback("UpdatedAccountPositionPushAddr")
def updated_account_position_push(data):
    send_cdata("UpdatedAccountPositionPush", data)
sp.register_updated_account_position_push(updated_account_position_push)


@sp.ffi.callback("UpdatedAccountBalancePushAddr")
def updated_account_balance_push(data):
    send_cdata("UpdatedAccountBalancePush", data)
sp.register_updated_account_balance_push(updated_account_balance_push)


@sp.ffi.callback("ApiTradeReportAddr")
def trade_report(rec_no, data):
    send_cdata("TradeReport", data)
sp.register_trade_report(trade_report)


@sp.ffi.callback("ApiPriceUpdateAddr")
def api_price_update(data):
    send_cdata("PriceUpdate", data)
sp.register_price_update(api_price_update)


@sp.ffi.callback("ApiTickerUpdateAddr")
def api_ticker_update(data):
    send_cdata("TickerUpdate", data)
sp.register_ticker_update(api_ticker_update)


@sp.ffi.callback("PswChangeReplyAddr")
def psw_change_reply(ret_code, ret_msg):
    send_cdata("PswChangeReply", {"ret_code" : ret_code,
                                  "ret_msg" : ret_msg})
sp.register_psw_change_reply(psw_change_reply)


@sp.ffi.callback("ProductListByCodeReplyAddr")
def product_list_by_code(inst_code, is_ready, ret_msg):
    data = {
        "inst_code": inst_code,
        "is_ready": is_ready,
        "ret_msg": ret_msg,
        "data": sp.get_product()}
    send_dict("ProductListByCodeReply", data)
sp.register_product_list_by_code_reply(product_list_by_code)


@sp.ffi.callback("InstrumentListReplyAddr")
def instrument_list_reply(is_ready, ret_msg):
    data = {"is_ready": is_ready,
            "ret_msg": ret_msg,
            "data": sp.get_instrument()}
    send_dict("InstrumentListReply", data)
sp.register_instrument_list_reply(instrument_list_reply)


@sp.ffi.callback("BusinessDateReplyAddr")
def business_date_reply(business_date):
    send_dict("BusinessDateReply", {
        "business_date": business_date
        })
sp.register_business_date_reply(business_date_reply)


@sp.ffi.callback("ApiMMOrderBeforeSendReportAddr")
def api_mm_order_before_send_report(mm_order):
    send_cdata("MMOrderBeforeSendReport", mm_order)
sp.register_mm_order_before_send_report(api_mm_order_before_send_report)


@sp.ffi.callback("ApiMMOrderRequestFailedAddr")
def api_mm_order_request_failed(mm_order, err_code, err_msg):
    send_dict("MMOrderRequestFailed",
              {"data": sp.cdata_to_py(mm_order[0]),
               "err_code": sp.cdata_to_py(err_code),
               "err_msg": sp.cdata_to_py(err_msg)})
sp.register_mm_order_request_failed(api_mm_order_request_failed)


@sp.ffi.callback("ApiQuoteRequestReceivedAddr")
def quote_request_received(product_code, buy_sell, qty):
    send_dict("QuoteRequestReceived",
              {"product_code": product_code,
               "buy_sell": buy_sell,
               "qty": qty})
sp.register_quote_request_received_report(quote_request_received)


def monitor_file(filename, newdata=False):
    try:
        tickerfile = open(filename)
    except FileNotFoundError:
        open(filename, 'a').close()
        tickerfile = open(filename)
    if newdata:
        tickerfile.seek(0, 2)

    def gen():
        try:
            while True:
                line = tickerfile.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                yield line
        except GeneratorExit:  # Or maybe use flask signals
            tickerfile.close()
    return Response(gen(), mimetype="text/plain")


# -------
@app.route("/login", methods=['POST'])
def login():
    if not request.form:
        abort(400)
    sp.set_login_info(request.form["host"],
                      int(request.form["port"]),
                      request.form["license"],
                      request.form["app_id"],
                      request.form["user_id"],
                      request.form["password"])
    return jsonify({"retval": sp.login()})


@app.route("/ping")
def ping():
    msg = {
        "msg": "Ping"
        }
    for sub in log_subscriptions[:]:
        sub.put(("ping", msg))
    return "OK"


@app.route("/logout")
def logout():
    global info_cache
    info_cache = empty_cache
    sp.logout()
    return "OK"

# ----------- Ticker code------


@sp.ffi.callback("ApiTickerUpdateAddr")
def ticker_update(data):
    send_cdata("ApiTickerUpdate", data)
    t = sp.cdata_to_py(data[0])
    tickerfile = open(get_ticker(t['ProdCode']), "a")
    dt = datetime.datetime.fromtimestamp(float(t['TickerTime']))
    price = "%.2f" % float(t['Price'])
    tickerfile.write("%s; %s; %s; %s; %s; %d\n" %
                     (dt.strftime("%Y/%m/%d/%H/%M/%S"),
                      price,
                      price,
                      price,
                      price,
                      int(t['Qty'])))
    tickerfile.close()
sp.register_ticker_update(ticker_update)


@app.route("/ticker/subscribe/<string:products>")
def subscribe_ticker(products):
    for p in products.split(","):
        ticker_products.add(p)
        if sp.ready() == 0:
            sp.subscribe_ticker(p, 1)
    if sp.ready() != 0:
        return "NOLOGIN"
    else:
        send_dict("TickerUpdate",
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
        send_dict("TickerUpdate",
                  {"data": list(ticker_products)})
        return "OK"


@app.route("/ticker/list")
def list_ticker():
    return jsonify({"data": list(ticker_products)})


@app.route("/ticker/view/<string:product>")
def view_ticker(product):
    return monitor_file(get_ticker(product))


@app.route("/ticker/clear/<string:product>")
def clear_ticker(product):
    fo = open(get_ticker(product), "w")
    fo.truncate()
    fo.close()
    return "OK"

# ----------- Strategy ------


class StrategyList(object):
    def __init__(self):
        self.stratlist = {}

    def start(self, kwargs):
        if id not in self.stratlist or \
               self.stratlist[id][0] is None:
            (p, q) = strategy.run(kwargs)
            kwargs['status'] = 'running'
            kwargs['comment'] = ''
            strategy_id = kwargs['id']
            self.stratlist[strategy_id] = (p, q, kwargs)
            t = threading.Thread(target=strategy_listener, args=(p, q))
            t.daemon = True
            t.start()
            send_dict("LocalStrategyStatus",
                      {"strategy": kwargs['strategy'],
                       "id": kwargs['id'],
                       "status": "running",
                       "comment": ""})
            return "OK"

    def stop(self, info, terminate=False):
        sid = info.get('id', None)
        if sid in self.stratlist:
            (p, q, cache) = self.stratlist[sid]
            cache['status'] = info['status']
            cache['comment'] = info['comment']
            info = cache
            if q is not None:
                q.close()
            if p is not None and terminate:
                p.terminate()
                p.join()
        self.stratlist[sid] = (None, None, info)
        send_dict("LocalStrategyStatus",
                  {"strategy": info['strategy'],
                   "id": info['id'],
                   "status": info['status'],
                   "comment" : info['comment']})
        return "OK"

    def data(self, stratname):
        retval = []
        for k, v in self.stratlist.items():
            if v[2]['strategy'] == stratname:
                retval.append(v[2])
        return retval

    def terminate_all(self):
        for k, v in self.stratlist.items():
            if v[0] is not None:
                p = v[0]
                p.terminate()
                p.join()

    def pause(self, f):
        raise NotImplementedError

stratlist = StrategyList()


def strategy_listener(p, q):
    try:
        while True:
            (s, sid, status, comment) = q.get()
            info = {"strategy": s,
                    "id": sid,
                    "status": status,
                    "comment": comment}
            if status == "error":
                stratlist.stop(info, terminate=True)
                return
            elif status == "done":
                stratlist.stop(info, terminate=False)
                return
    except GeneratorExit:  # Or maybe use flask signals
        return


@app.route("/strategy/start", methods=['POST'])
def strategy_start():
    if not request.form:
        abort(400)
    return stratlist.start(request.form.to_dict())


@app.route("/strategy/stop", methods=['POST'])
def strategy_stop():
    if not request.form:
        abort(400)
    f = request.form.to_dict()
    f['status'] = "done"
    f['comment'] = ""
    return stratlist.stop(f, terminate=True)


@app.route("/strategy/pause", methods=['POST'])
def strategy_pause():
    if not request.form:
        abort(400)
    return stratlist.pause(request.form.to_dict())


@app.route("/strategy/log/<string:strategy_id>")
def strategy_log(strategy_id):
    return monitor_file(os.path.join(data_dir,
                                     "log-%s.txt" % strategy_id))


@app.route("/strategy/list")
def strategy_list():
    return json.dumps(strategy.strategy_list())


@app.route('/strategy/headers/<string:stratname>')
def strategy_headers(stratname):
    return json.dumps(strategy.headers(stratname))


@app.route('/strategy/data/<string:stratname>')
def strategy_data(stratname):
    return json.dumps({"data": stratlist.data(stratname)})


# -----------------------------
@app.route("/backtest", methods=['POST'])
def backtest():
    return strategy.backtest(request.form.to_dict())


# ---------------------------
@app.route("/orders/read")
def orders_read():
    pass


# ---------------------------
@app.route("/trade/list")
def list_trade():
    return jsonify({"data": sp.get_all_trades()})


# -----------------

@app.route("/order/list")
def order_list():
    return jsonify({"data": sp.get_all_orders()})


@app.route("/order/add", methods=['POST'])
def order_add():
    if request.form:
        f = request.form.to_dict()
    elif request.json:
        f = request.json
    else:
        abort(400)
    return str(sp.order_add(f))


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
        sp.subscribe_price(p, 0)
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
                (event_id, result) = q.get()
                ev = ServerSentEvent(result, event_id)
                yield ev.encode()
        except GeneratorExit:  # Or maybe use flask signals
            log_subscriptions.remove(q)
    return Response(gen(), mimetype="text/event-stream")


@app.route("/schema/<string:structure>")
def schema(structure):
    return jsonify({"retval": sp.fields(structure)})


@app.route("/exit")
def exit_done():
    exit()
    return "OK"

if __name__ == "__main__":
    try:
        app.debug = True
        app.run(threaded=True)
    except KeyboardInterrupt:
        stratlist.terminate_all()
