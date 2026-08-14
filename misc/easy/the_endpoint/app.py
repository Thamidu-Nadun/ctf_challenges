import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return f"Hello User, This is {os.getenv('INSTANCE', 'NULL')} instance!"


@app.route("/flag")
def flag():
    return jsonify("FLAG{this_is_a_secret_flag}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
