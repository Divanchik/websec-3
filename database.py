import datetime
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
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


def find_user_by_name(user):
    user = db_session.query(User.username, User.email, User.password).select_from(
        User).where(User.username == user).all()
    result = []
    for i in user:
        result.append(i[0])
        result.append(i[1])
        result.append(i[2])
    print(result)
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
    return result

def is_username_exist(username):
    check = db_session.query(User.username, User.email, User.password).select_from(
        User).where(User.username == username).all()
    if len(check) == 0:
        return False
    return True

def is_email_exist(email):
    check = db_session.query(User.username, User.email, User.password).select_from(
        User).where(User.email == email).all()
    if len(check) == 0:
        return False
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
    data = Column(DateTime, default=datetime.datetime.utcnow)
    likes_count = Column(Integer)
    u_id = Column(Integer, ForeignKey('users.userID'))
    user = relationship('User')

    def __init__(self, content, user, likes_count=0):
        self.content = content
        self.likes_count = likes_count
        self.user = user


class Image(Base):
    __tablename__ = "images"
    imageID = Column(Integer, primary_key=True)
    imageURL = Column(String(100), nullable=True)
    order = Column(Integer)  # Zachem??
    p_id = Column(Integer, ForeignKey('posts.postID'))
    post = relationship('Post')
    u_id = Column(Integer, ForeignKey('users.userID'))
    user = relationship('User')

    def __init__(self, URL, ord, post, user):
        self.imageURL = URL
        self.order = ord
        self.post = post
        self.user = user


class Subscription(Base):
    __tablename__ = "subscriptions"
    sub_id = Column(Integer, primary_key=True)
    #subscriber_id = Column(Integer,ForeignKey('users.userID'))
    subscription_id = Column(Integer, ForeignKey('users.userID'))
    #subscriber = relationship('User')
    subscription = relationship('User')

    def __init__(self,  subscription) -> None:
        #self.subscriber = subscriber
        self.subscription = subscription


class Subscriber(Base):
    __tablename__ = "subscribers"
    sub_id = Column(Integer, primary_key=True)
    subscriber_id = Column(Integer, ForeignKey('users.userID'))

    def __init__(self,  subscriber) -> None:
        self.subscriber = subscriber


class Comment(Base):
    __tablename__ = "comments"
    commentID = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=True)
    dataComment = Column(DateTime, default=datetime.datetime.utcnow)
    p_id = Column(Integer, ForeignKey('posts.postID'))
    post = relationship('Post')
    author_id = Column(Integer, ForeignKey('users.userID'))
    user = relationship('User')

    def __init__(self, content, user, post):
        self.content = content
        self.user = user
        self.post = post


class Like(Base):
    __tablename__ = "likes"
    p_id = Column(Integer, ForeignKey('posts.postID'), primary_key=True)
    post = relationship('Post')
    u_id = Column(Integer, ForeignKey('users.userID'), primary_key=True)
    user = relationship('User')

    def __init__(self, user, post):
        self.user = user
        self.post = post

# init_db()
#u = User('Goshan', 'admin@ocalhost.ru', "34ggq32q")
# db_session.add(u)
# db_session.commit()
