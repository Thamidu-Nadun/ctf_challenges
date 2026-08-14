from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__, template_folder="templates")


def ping_host(host):
    try:
        res = subprocess.run(
            f"ping -c 1 {host}", shell=True, capture_output=True, text=True
        )
        out = res.stdout + res.stderr
        return out
    except Exception as e:
        return str(e)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        host = request.form.get("host")
        output = ping_host(host)
        return render_template("index.html", output=output)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
