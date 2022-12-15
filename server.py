from flask import Flask, render_template, redirect, session, request
from json import dumps
import sqlite3

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.get("/login")
def login():
    return render_template("login.html")

@app.post("/login")
def login_data():
    app.logger.debug("Got login data!")
    data = request.get_json()
    for k, v in data.items():
        print(f"\t{k}: {v}")
    return dumps({'success': True, 'username': 'dimadivan'})

@app.get("/register")
def register():
    return render_template("register.html")

@app.post("/register")
def register_data():
    app.logger.debug("Got register data!")
    data = request.get_json()
    for k, v in data.items():
        print(f"\t{k}: {v}")
    return dumps({'success': False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)