from flask import Flask, Response
app = Flask(__name__)
import os
import sys
import sse
location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)

import gevent
from gevent.queue import Queue
from gevent.wsgi import WSGIServer
from sse import ServerSentEvent
import sptrader

sptrader = None
subscriptions = []



@app.route("/")
def hello():
    return app.send_static_file("sptrader.html")

@app.route("/login", methods=['POST'])
def login():
    if not request.json:
        abort(400)
    if sptrader != None:
        abort(400)
    sptrader = sptrader.SPTrader(request.json("host"),
                                 request.json("port"),
                                 request.json("license"),
                                 request.json("app_id"),
                                 request.json("user_id"),
                                 request.json("password"))
    return jsonify({"retval" : sptrader.login()})

@app.route("/ping")
def ping():
    msg = {
        "id" : "ping",
        "msg" : "Ping"
        }
    for sub in subscriptions[:]:
        sub.put(msg)
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
    server = WSGIServer(("", 5000), app)
    server.serve_forever()

