
#This service belongs only for "Monitoring system". The only way a player access to this through watchtower-gw

#Every endpoint ask header X-WT-Key: <WATCHTOWER_API_KEY> 
#Player recieves it from S5 web exploit


#  Flag: inside of the evidence package -> RAVEN{you_were_the_attacker}

import os, json, functools
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

API_KEY = os.environ.get("WATCHTOWER_API_KEY", "changeme")
SEED = os.path.join(os.path.dirname(__file__), "seed")

def load(name):
    with open(os.path.join(SEED, name), "r", encoding="utf-8") as f:
        return f.read()

def require_key(fn):
    
    @functools.wraps(fn)
    def wrapper(*a, **kw):
        key = request.headers.get("X-WT-Key", "")
        if key != API_KEY:
            return jsonify({
                "error": "WATCHTOWER access denied",
                "reason": "missing or invalid X-WT-Key",
                "hint": "This key is an S5 artifact (recovered from the portal)."
            }), 403
        return fn(*a, **kw)
    return wrapper

@app.route("/")
def banner():
    return jsonify({
        "service": "WATCHTOWER",
        "segment": "monitoring (not externally exposed)",
        "auth": "all data endpoints require header  X-WT-Key",
        "endpoints": ["/telemetry", "/operations/nightfall", "/evidence"]
    })

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/telemetry")
@require_key
def telemetry():
    return Response(load("telemetry.json"), mimetype="application/json")

@app.route("/operations/nightfall")
@require_key
def nightfall():
    return Response(load("nightfall_oplog.json"), mimetype="application/json")

@app.route("/evidence")
@require_key
def evidence():
    return Response(load("evidence_package.txt"), mimetype="text/plain")

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=9000)
