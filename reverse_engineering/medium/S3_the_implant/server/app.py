#!/usr/bin/env python3

#  RAVEN//TRACE — S3 "THE IMPLANT" :: register server

#  Flag:  RAVEN{the_implant_knows_you}

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

RAVEN_ID     = os.environ.get("RAVEN_ID", "RAVEN-17")
GDN_CLIENT   = os.environ.get("GDN_CLIENT", "guardian_update")
ACTIVATION   = os.environ.get("ACTIVATION_CODE", "USFE-INV-07")
FLAG         = os.environ.get("FLAG", "RAVEN{the_implant_knows_you}")

@app.route("/")
def banner():
    return jsonify({"service": "GuardianOS registration node", "status": "online"})

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/api/v3/register", methods=["POST"])
def register():
    raven = request.headers.get("X-Raven-ID", "")
    gdn   = request.headers.get("X-GDN-Client", "")
    auth  = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        auth = auth[7:].strip()

    if raven == RAVEN_ID and gdn == GDN_CLIENT and auth == ACTIVATION:
        return jsonify({"status": "registered", "flag": FLAG})

    return jsonify({
        "error": "registration rejected",
        "hint": "Reverse guardian_update.exe — the server only accepts the "
                "exact headers the client was built to send "
                "(X-Raven-ID, X-GDN-Client, Authorization)."
    }), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
