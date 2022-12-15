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

@app.post("/login")
def login_data():
    # check, if login is email or username
    # search for user
    # check password
    # set flag and username (for link)
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
<<<<<<< HEAD
    # check email and username uniqueness
    # if alright, generate link and send mail
    # set success flag
    app.logger.debug("Got register data!")
    data = request.get_json()
    for k, v in data.items():
        print(f"\t{k}: {v}")
=======
    app.logger.debug("register [POST]")
    print(request.get_json())
    mail.send_email(request.get_json()['username'], request.get_json()['email'], request.get_json()['password'])
>>>>>>> 3e93370146027709b13cf8e97529edee93b7165f
    return dumps({'success': False})

@app.get("/confirm")
def confirmation():
    # check data from link
    # add user to db (or not)
    # make confirmation message (successful or not, etc)
    return render_template("confirm.html", conf_msg="Registration confirmed!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)