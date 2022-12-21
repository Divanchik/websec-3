from flask import Flask, render_template, redirect, session, request, url_for
from json import dumps
import mail
import database
import hashlib
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["UPLOAD_FOLDER"] = "./images"
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
    session["id"] = hashlib.sha256(user[0].encode("utf-8") + salt.encode("utf-8")).hexdigest()
    return dumps({'success': True, 'username':user[0]})

@app.get("/user/<username>")
def user(username):
    isauthor = True if session["username"] == username else False
    return render_template("userprofile.html", pagetitle=f"{username}'s profile", username=username, author=isauthor)


@app.get("/image/<image_number>")
def get_image(image_number):
    image_path = database.get_image_name(image_number)
    with open(image_path, "rb") as f:
        image = f.read()
    return image
@app.post("/user/<username>")
def get_post(username):
    if request.get_json()['action'] == 'getposts':
        res = database.get_posts_by_user(username)
        return dumps(res)
    elif request.get_json()['action'] == 'like':
        likes_count = database.count_of_likes(request.get_json()['postnum'])
        if database.is_liked(session["username"], request.get_json()['postnum']):
            database.add_like(session["username"], request.get_json()['postnum'])
            likes_count += 1
        else:
            database.delete_like(session["username"], request.get_json()['postnum'])
            likes_count -= 1
        return dumps({'success': True, 'likes': likes_count})
    

@app.get("/logout")
def logout():
    session.pop('username', None)
    session.pop('id', None)
    return render_template("login.html")

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

@app.get("/user/<username>/new")
def post(username):
    return render_template("newpost.html")


@app.post("/user/<username>/new")
def new_post(username):
    image_id = 0
    image = request.files.get('pub_img')
    print(request.form['post_content'])
    if image.filename != "":
        format = image.filename.endswith(".png")
        name = hashlib.sha256(database.count_of_images().encode()).hexdigest()
        if format:
            filename = f'{app.config["UPLOAD_FOLDER"]}/{name}.png'
            image.save(filename)
            image_id = database.add_image(filename)
        else:
            filename = f'{app.config["UPLOAD_FOLDER"]}/{name}.jpeg'
            image.save(filename)
            image_id = database.add_image(filename)
    
    database.add_post(username,request.form['post_content'], image_id)
    
    
    return redirect(url_for('user', username=username))
if __name__ == "__main__":
    database.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)