from flask import Flask
app = Flask(__name__)
location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, location)
import sptrader
sptrader = None

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
                    

if __name__ == "__main__":
    app.run()
