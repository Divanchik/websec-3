from flask import Flask, render_template, redirect, session, request
from json import dumps
import sqlite3
import mail
import dbScriptr
app = Flask(__name__)
salt = "e&xKRt*kb&tUlrQ6"
@app.route("/")
def main():
    return render_template("index.html")
@app.route("/confirm")
def test():
    username = request.args.getlist("username")[0]
    email = request.args.getlist("email")[0]
    hash_passwd = request.args.getlist("hash_passwd")[0]
    print(type(hash_passwd))
    data = request.args.getlist("data")[0]
    flag = mail.confirm_link(username, email, hash_passwd, data, mail.salt)
    print(flag)
    if flag == True:
        test = f"Добро пожаловать в dwitter, {username}"
        dbScriptr.add_user(username, email, hash_passwd)
    else:
        test = "Возникли проблемы с регистрацией, попробуйте еще раз!"
    return render_template("confirm.html", test=test)
@app.get("/login")
def login():
    return render_template("login.html")

@app.get("/register")
def register():
    return render_template("register.html")

@app.post("/register")
def register_data():
    app.logger.debug("register [POST]")
    print(request.get_json())
    mail.send_email(request.get_json()['username'], request.get_json()['email'], request.get_json()['password'])
    return dumps({'success': False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)