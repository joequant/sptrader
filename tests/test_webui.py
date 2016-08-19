from flask import Flask, Response, jsonify, request, abort


import os
import sys
import cffi

location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(location, "..", "sptrader"))

import sse
import config
from queue import Queue
from sse import ServerSentEvent
import sptrader
import config

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
        ret_msg =  sp.ffi.string(ret_msg).decode('utf-8')

    msg = {
        "id" : "LoginReply",
        "ret_code" : ret_code,
        "ret_msg" : ret_msg
        }
    for sub in subscriptions[:]:
        sub.put(msg)
sp.register_login_reply(login_reply)

@sp.ffi.callback("ConnectedReplyAddr")
def connected_reply(host_type, con_status):
    msg = {
        "id" : "ConnectedReply",
        "host_type" : host_type,
        "con_status" : con_status
        }
    for sub in subscriptions[:]:
        sub.put(msg)
sp.register_connecting_reply(connected_reply)

@sp.ffi.callback("AccountInfoPushAddr")
def account_info_push(data):
    msg = {
        "id" : "AccountInfoPush",
        "NAV" : data[0].NAV,
        "CreditLimit" : data[0].CreditLimit,
        "ClientId" : sp.ffi.string(data[0].ClientId).decode('utf-8'),
        "MarginClass" : sp.ffi.string(data[0].MarginClass).decode('utf-8')
        }
    for sub in subscriptions[:]:
        sub.put(msg)
sp.register_account_info_push(account_info_push)

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
    return jsonify({"retval" : sp.login()})

@app.route("/get-login-status/<int:host_id>")
def get_login_status(host_id):
    global sp
    if host_id not in [80, 81, 83, 87, 88]:
        return "-1"
    return "%d" % sp.get_login_status(host_id)

@app.route("/ping")
def ping():
    msg = {
        "id" : "ping",
        "msg" : "Ping"
        }
    for sub in subscriptions[:]:
        sub.put(msg)
    return "OK"

@app.route("/logout")
def logout():
    global sp
    sp.logout()
    return "OK"
    
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

