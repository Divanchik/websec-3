import hashlib 
import smtplib
import os
from email.mime.text import MIMEText
import json

def get_link(username:str, email:str, password:str):
    salt = os.urandom(16)
    with open ("key.bin", "wb") as f:
        f.write(salt)
    hash_passwd = hashlib.sha256(password.encode() + salt)
    checksum = hashlib.sha3_256(hash_passwd.hexdigest().encode() + username.encode() + password.encode())
    return f"http://localhost:5000/?username={username}&email={email}&hash_passwd={hash_passwd.hexdigest()}&data={checksum.hexdigest()}" 

def send_email(username:str, email:str, password:str):
    with open("mail.json","r") as f:
        data = f.read()
    data = json.loads(data)
    sender = data["mail"]
    passw = data["password"]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, passw)
        msg = MIMEText(get_link(username, email, password))
        server.sendmail(sender, email, msg.as_string())
        return "The message was sent successfully!"
    except Exception as _ex:
            return f"{_ex}\nCheck your login or password please!"

#print(get_link("shafa_01", "shafranyukroman@yandex.ru","12345678"))
print(send_email("shafa_01", "shafranyukroman@yandex.ru","12345678"))