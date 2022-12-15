from flask import Flask, render_template, redirect, session, request, url_for
from json import dumps
import mail
import database
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
salt = "e&xKRt*kb&tUlrQ6"
@app.route("/")
def main():
    return render_template("index.html")
@app.route("/confirm")
def confirm():
    username = request.args.getlist("username")[0]
    email = request.args.getlist("email")[0]
    hash_passwd = request.args.getlist("hash_passwd")[0]
    print(type(hash_passwd))
    data = request.args.getlist("data")[0]
    if  mail.confirm_link(username, email, hash_passwd, data, mail.salt):
        message = f"Добро пожаловать в dwitter, {username}"
        database.add_user(username, email, hash_passwd)
    else:
        message = "Возникли проблемы с регистрацией, попробуйте еще раз!"
    return render_template("confirm.html", conf_msg=message)

@app.get("/login")
def login():
    return render_template("login.html")


@app.post("/login")
def login_data():
    data = request.get_json()['login']
    passwd= request.get_json()['password']
    if "@" in data:
        user = database.find_user_by_email(data)
    else:
        user = database.find_user_by_name(data)
    if len(user) == 0:
       return dumps({'success': False})
    if mail.check_passwd(passwd,user[2]) == False:
        return dumps({'success': False})
    session["username"] = user[0]
    return dumps({'success': True, 'username':user[0]})

@app.get("/register")
def register():
    return render_template("register.html")

@app.post("/register")
def register_data():
    app.logger.debug("register [POST]")
    print(request.get_json())
    if database.is_username_exist(request.get_json()['username']) or database.is_email_exist(request.get_json()['email']):
        return dumps({'success': False})
    mail.send_email(request.get_json()['username'], request.get_json()['email'], request.get_json()['password'])
    return dumps({'success': True})

if __name__ == "__main__":
    database.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)