import sqlite3

def create_database():
    db = sqlite3.connect('dwitter.db')

    cursor = db.cursor()

    cursor.execute("""CREATE TABLE users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""CREATE TABLE posts (
        postID INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        data TEXT NOT NULL,
        likesCount INTEGER,
        u_id INTEGER, 
        FOREIGN KEY (u_id) REFERENCES users (userID)
    )
    """)

    cursor.execute("""CREATE TABLE images (
        imageID INTEGER PRIMARY KEY AUTOINCREMENT,
        imageURL TEXT NOT NULL,
        ord INTEGER,
        p_id INTEGER,
        FOREIGN KEY (p_id) REFERENCES posts (postID)
        
    )
    """)

    cursor.execute("""CREATE TABLE subscriptions (
        subscriber_id INTEGER,
        subscription_id INTEGER,
        FOREIGN KEY (subscriber_id) REFERENCES users (userID),
        FOREIGN KEY (subscription_id) REFERENCES users (userID)
    )
    """)

    cursor.execute("""CREATE TABLE comments (
        commentID INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        dataComment TEXT NOT NULL,
        p_id INTEGER,
        author_id INTEGER,
        FOREIGN KEY (p_id) REFERENCES posts (postID),
        FOREIGN KEY (author_id) REFERENCES users (userID)

    )
    """)

    cursor.execute("""CREATE TABLE likes (
        p_id INTEGER,
        u_id INTEGER,
        FOREIGN KEY (p_id) REFERENCES posts (postID),
        FOREIGN KEY (u_id) REFERENCES users (userID)
    )
    """)
    db.commit()
    db.close()

def check_repeatings(username, email):
    pass
def add_user(username:str, email:str, hash_passwd:str):
    db = sqlite3.connect('dwitter.db')
    cursor = db.cursor()
    query = (f"""INSERT INTO users (username, email, password) VALUES('{username}','{email}','{hash_passwd}');""")
    cursor.execute(query)
    cursor.close()
    db.commit()
    db.close()

def get_data():
    db = sqlite3.connect('dwitter.db')
    cursor = db.cursor()
    res = cursor.execute("""SELECT * FROM users""")
    print(res.fetchall())
    cursor.close()
    db.close()
#create_database()
get_data()
#add_user("Gosha", "kaktotam@mail.ru", "5d345rg4rg231twqe")