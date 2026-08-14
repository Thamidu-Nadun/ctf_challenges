from flask import Flask, render_template, request

from db import setup_db, get_db

app = Flask(__name__, template_folder="templates", static_folder="static")


def login(username, password):
    conn = get_db()
    cursor = conn.cursor()
    query = (
        f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    )
    cursor.execute(query)

    user = cursor.fetchone()
    if user:
        print(f"Welcome, {username}!")
        return True
    else:
        print("Invalid username or password")
        return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    username = request.form.get("username")
    password = request.form.get("password")
    user = login(username, password)
    if user:
        cursor.execute("SELECT key, value FROM config;")
        config = cursor.fetchall()
        config_dict = {row[0]: row[1] for row in config}
        return render_template("dashboard.html", config=config_dict)
    return render_template("index.html", error="Invalid username or password")


if __name__ == "__main__":
    setup_db()
    app.run(debug=True, port=5000)
