import hashlib 
import smtplib
import os
from email.mime.text import MIMEText
import json

salt = "e&xKRt*kb&tUlrQ6"


def get_link(username:str, email:str, password:str, salt:str):
    #salt = os.urandom(16)
    hash_passwd = hashlib.sha256(password.encode("utf-8") + salt.encode("utf-8"))
    data = username.encode("utf-8") + email.encode("utf-8") + hash_passwd.hexdigest().encode("utf-8")
    data_hash = hashlib.sha256(data + salt.encode("utf-8"))
    return f"http://localhost:5000/confirm?username={username}&email={email}&hash_passwd={hash_passwd.hexdigest()}&data={data_hash.hexdigest()}" 

def confirm_link(username:str, email:str, phash:str, dhash: str, salt: str):
    print(f"Пользователь:{username}")
    print(f"Email:{email}")
    print(f"Хэш-пароль:{phash}")
    print(f"Checksum:{dhash}")
    print(F"Salt:{salt}")
    data = username.encode("utf-8") + email.encode("utf-8") + phash.encode("utf-8")
    data_hash = hashlib.sha256(data + salt.encode("utf-8"))
    print(f"Контрольная сумма: {data_hash.hexdigest()}")
    if data_hash.hexdigest() == dhash:
        return True
    return False

def send_email(username:str, email:str, password:str):
    with open("mail.json","r") as f:
        data = f.read()
    data = json.loads(data)
    sender = data["mail"]
    passw = data["password"]
    server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
    #server.starttls()
    text = f"""
       <!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
    </head>
<body>
    <h1>Подтвердите регистрацию в dwitter!</h1>
    <a href="{get_link(username, email, password, salt)}"><button type="button" class="btn btn-info" >Подтвердить</button></a>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3"
    crossorigin="anonymous"></script>
</body>

</html>
    
    """

    try:
        server.login(sender, passw)
        msg = MIMEText(text, "html")
        server.sendmail(sender, email, msg.as_string())
        return "The message was sent successfully!"
    except Exception as _ex:
            return f"{_ex}\nCheck your login or password please!"



def check_passwd(passwd:str, hashpasswd):
     
    check_hash_passwd = hashlib.sha256(passwd.encode("utf-8") + salt.encode("utf-8"))

    if check_hash_passwd.hexdigest() == hashpasswd:
        return True
    return False
#print(get_link("shafa_01", "shafranyukroman@yandex.ru","12345678"))
#print(send_email("shafa_01", "jimmycerry999@gmail.com","12345678"))