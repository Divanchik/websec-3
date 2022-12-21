import datetime
from sqlalchemy import create_engine, DateTime, delete
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.functions import count
engine = create_engine('sqlite:///test.db')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


def add_user(username, email, hashpasswd):
    u = User(username, email, hashpasswd)
    db_session.add(u)
    db_session.commit()


def add_post(author_name, content, im_id):
    author = db_session.query(User.userID).select_from(
        User).where(User.username == author_name).all()
    author_id = author[0][0]
    new_post = Post(content, author_id, im_id)
    db_session.add(new_post)
    db_session.commit()

def add_like(username, p_id):
    u_id = db_session.query(User.userID).select_from(User).where(User.username == username).all()
    new_like = Like(u_id[0][0], p_id)
    db_session.add(new_like)
    db_session.commit()

def add_image(URL):
    new_image = Image(URL)
    db_session.add(new_image)
    db_session.commit()
    image_id = db_session.query(Image.imageID).select_from(
        Image).where(Image.imageURL == URL).all()
    db_session.commit()
    return image_id[0][0]

def add_comment(username, post_id, content):
    u_id = db_session.query(User.userID).select_from(User).where(User.username == username).all()
    new_comment = Comment(content, u_id[0][0], post_id)
    db_session.add(new_comment)
    db_session.commit() 



def delete_like(username, p_id):
    u_id = db_session.query(User.userID).select_from(User).where(User.username == username).all()
    deleted = delete(Like).where(Like.p_id == p_id and Like.u_id == u_id[0][0])
    db_session.execute(deleted)
    db_session.commit()

def count_of_images():
    c = db_session.query(count(Image.imageID)).select_from(Image).all()
    db_session.commit()
    return str(c[0][0])

def count_of_likes(p_id):
    likes_count = db_session.query(count(Like.u_id)).select_from(Like).where(Like.p_id == p_id).all()
    db_session.commit()
    return likes_count[0][0]

def is_liked(username, p_id):
    u_id = db_session.query(User.userID).select_from(User).where(User.username == username).all()
    flag = db_session.query(count(Like.u_id)).select_from(Like).join(User).where(Like.p_id == p_id).where(Like.u_id == u_id[0][0]).all()
    print(f"Flag = {flag}")
    if flag[0][0] == 1:
        return True
    return False

def get_image_name(image_id):
    name = db_session.query(Image.imageURL).select_from(Image).where(Image.imageID == image_id).all()
    return name[0][0]

def get_comment(p_id):
    res = []
    comments_inf = db_session.query(User.username, Comment.content, Comment.dataComment).select_from(Comment).join(User).where(Comment.p_id == p_id).all()
    db_session.commit()
    for i in comments_inf:
        tmp = {}
        tmp["author"] = i[0]
        tmp["content"] = i[1]
        tmp["date"] = i[2].strftime(r"%Y-%m-%d %H:%M")
        res.append(tmp)
    res = sorted(
    res,
    key=lambda x: datetime.datetime.strptime(x['date'], r'%Y-%m-%d %H:%M'), reverse=False)
    #print(res)
    return res

def get_posts_by_user(author, username):
    result = []

    posts = db_session.query(User.username, Post.postID, Post.data, Post.content).select_from(
        User).join(Post).where(User.username == author).all()
    db_session.commit()
    
    posts_id = []
    authors = []
   

    for i in posts:
        authors.append(i[0])
        posts_id.append(i[1])
        tmp = {}
        tmp["author"] = i[0]
        tmp["post_id"] = i[1]
        tmp["datetime"] = i[2].strftime(r"%Y-%m-%d %H:%M")
        tmp["content"] = i[3]
        result.append(tmp)
    print(posts_id)
    
    for i in range(len(posts_id)):
        im_id = db_session.query(Image.imageID).select_from(Post).join(Image).where(Post.postID == posts_id[i]).all()
        db_session.commit()
        result[i]["image_id"] = im_id[0][0]

    for i in range(len(posts_id)):
        likes_count = db_session.query(count(Like.u_id)).select_from(Like).where(Like.p_id == posts_id[i]).all()
        db_session.commit()
        result[i]["likes"] = likes_count[0][0]

    for i in range(len(posts_id)):
        print(f"author: {authors[i]}\n post_id = {posts_id[i]}")
        u_id = db_session.query(User.userID).select_from(User).where(User.username == username).all()
        print(f"u_id:{u_id[0][0]}")
        flag = db_session.query(count(Like.u_id)).select_from(Like).join(User).where(Like.p_id == posts_id[i]).where(Like.u_id == u_id[0][0]).all()
        print(f"Flag:{flag}")
        if flag[0][0] == 1:
            result[i]["isliked"] = True
        else:
            result[i]["isliked"] = False
    
    print(result)

    return result


def find_user_by_name(user):
    user = db_session.query(User.username, User.email, User.password).select_from(
        User).where(User.username == user).all()
    result = []
    for i in user:
        result.append(i[0])
        result.append(i[1])
        result.append(i[2])
    print(result)
    db_session.commit()
    return result


def find_user_by_email(email):
    user = db_session.query(User.username, User.email, User.password).select_from(
        User).where(User.email == email).all()
    print(user)
    result = []
    for i in user:
        result.append(i[0])
        result.append(i[1])
        result.append(i[2])
    print(result)
    db_session.commit()
    return result


def is_username_exist(username):
    check = db_session.query(User.username, User.email, User.password).select_from(
        User).where(User.username == username).all()
    if len(check) == 0:
        db_session.commit()
        return False
    db_session.commit()
    return True


def is_email_exist(email):
    check = db_session.query(User.username, User.email, User.password).select_from(
        User).where(User.email == email).all()
    if len(check) == 0:
        db_session.commit()
        return False
    db_session.commit()
    return True


class User(Base):
    __tablename__ = 'users'
    userID = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Post(Base):
    __tablename__ = "posts"
    postID = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=True)
    data = Column(DateTime, default=datetime.datetime.now())
    likes_count = Column(Integer)
    u_id = Column(Integer, ForeignKey('users.userID'))
    user = relationship('User')
    im_id = Column(Integer, ForeignKey('images.imageID'))
    image = relationship('Image')

    def __init__(self, content, author_id, image, likes_count=0):
        self.content = content
        self.likes_count = likes_count
        self.u_id = author_id
        self.im_id = image


class Image(Base):
    __tablename__ = "images"
    imageID = Column(Integer, primary_key=True)
    imageURL = Column(String(100), nullable=True)

    def __init__(self, URL):
        self.imageURL = URL


class Subscription(Base):
    __tablename__ = "subscriptions"
    sub_id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey(
        'users.userID'), nullable=False)
    subscriber_id = Column(Integer, ForeignKey('users.userID'), nullable=False)
    subscription = relationship('User', foreign_keys=[subscription_id])
    subscriber = relationship('User', foreign_keys=[subscriber_id])

    def __init__(self,  subscription_id, subscriber) -> None:
        self.subscription_id = subscription_id
        self.subscriber_id = subscriber

class Comment(Base):
    __tablename__ = "comments"
    commentID = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=True)
    dataComment = Column(DateTime, default=datetime.datetime.now())
    p_id = Column(Integer, ForeignKey('posts.postID'))
    post = relationship('Post')
    author_id = Column(Integer, ForeignKey('users.userID'))
    user = relationship('User')

    def __init__(self, content, user_id, post_id):
        self.content = content
        self.author_id = user_id
        self.p_id = post_id


class Like(Base):
    __tablename__ = "likes"
    p_id = Column(Integer, ForeignKey('posts.postID'), primary_key=True)
    post = relationship('Post')
    u_id = Column(Integer, ForeignKey('users.userID'), primary_key=True)
    user = relationship('User')

    def __init__(self, user_id, post_id):
        self.u_id = user_id
        self.p_id = post_id


# init_db()
#u = User('Goshan', 'admin@ocalhost.ru', "34ggq32q")
# db_session.add(u)
# db_session.commit()
# get_posts_by_user('Roman')
#print(count_of_likes(1))
#print(is_liked('Roman', 3))
#add_like("Roman",1)
#add_like("Roman",2)
#add_like("Roman",3)
#delete_like("Roman",3)
#add_comment("Roman",3, 'Владимир Путин, молодец!')
#add_comment("Roman",3, 'Политик, лидер и борец!')
get_comment(3)