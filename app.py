import json
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "SENU_MODZ_SECRET_KEY"

USERNAME = "admin"
PASSWORD = "1234"
OWNER_NAME = "SENU MODZ"

# Load V2Ray configs
with open("v2ray_configs.json", "r") as f:
    vpn_configs = json.load(f)["vpn_configs"]

# Load VPN apps
with open("vpn_apps.json", "r") as f:
    vpn_apps = json.load(f)["apps"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials!")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", owner=OWNER_NAME, vpn_configs=vpn_configs, vpn_apps=vpn_apps)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
