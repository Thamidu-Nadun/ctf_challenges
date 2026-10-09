
#  "The C2 only answers something it recognises." (H1 hint)

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

RAVEN_ID    = os.environ.get("RAVEN_ID", "RAVEN-17")
IMPLANT_AUTH= os.environ.get("IMPLANT_AUTH", "USFE-INV-07")
GDN_CLIENT  = os.environ.get("GDN_CLIENT", "guardian_update")


# after C2 regitration, below next hop details are given to the user.
GW_HOST = os.environ.get("GW_HOST", "watchtower-gw")
GW_USER = os.environ.get("GW_USER", "svc_watch")
GW_PASS = os.environ.get("GW_PASS", "R3lay#W4tch_2026")
WT_HOST = os.environ.get("WT_HOST", "watchtower")
WT_PORT = os.environ.get("WT_PORT", "9000")

@app.route("/")
def banner():
    return jsonify({
        "service": "GuardianOS sync node",
        "status": "online",
        "note": "nothing to see here"   # themed misdirection
    })

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/api/v3/register", methods=["POST"])
def register():
    raven = request.headers.get("X-Raven-ID", "")
    auth  = request.headers.get("Authorization", "")
    gdn   = request.headers.get("X-GDN-Client", "")

    
    if auth.lower().startswith("bearer "):
        auth = auth[7:].strip()

    if raven != RAVEN_ID or auth != IMPLANT_AUTH or gdn != GDN_CLIENT:
        
        return jsonify({
            "error": "unrecognised implant",
            "hint": "The C2 only answers something it recognises. "
                    "Replay the registration exactly as the implant did "
                    "(X-Raven-ID, Authorization, X-GDN-Client)."
        }), 401

    
    return jsonify({
        "status": "registered",
        "operator": RAVEN_ID,
        "message": "Implant acknowledged. WATCHTOWER is on the monitoring "
                   "segment and is NOT reachable from here directly. "
                   "Pivot through the gateway below.",
        "pivot": {
            "gateway_host": GW_HOST,
            "ssh_user": GW_USER,
            "ssh_pass": GW_PASS,
            "note": "SSH to the gateway; it bridges into the monitoring segment."
        },
        "watchtower": {
            "host": WT_HOST,
            "port": int(WT_PORT),
            "auth_header": "X-WT-Key",
            "auth_value_source": "S5 artifact (WATCHTOWER_API_KEY) — not issued here"
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
