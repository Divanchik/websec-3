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

def add_post(author_name, content):
    author = db_session.query(User.userID).select_from(User).where(User.username == author_name).all()
    author_id = author[0][0]
    new_post = Post(content, author_id)
    db_session.add(new_post)
    post_id = db_session.query(Post.postID).select_from(Post).where(Post.content == content).all()
    post_id = post_id[0][0]
    db_session.commit()
    return post_id

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

    def __init__(self, content, author_id, likes_count=0):
        self.content = content
        self.likes_count = likes_count
        self.u_id = author_id


class Image(Base):
    __tablename__ = "images"
    imageID = Column(Integer, primary_key=True)
    imageURL = Column(String(100), nullable=True)
    order = Column(Integer)  # Zachem??
    p_id = Column(Integer, ForeignKey('posts.postID'))
    post = relationship('Post')
    u_id = Column(Integer, ForeignKey('users.userID'))
    user = relationship('User')

    def __init__(self, URL, ord, post_id, user):
        self.imageURL = URL
        self.order = ord
        self.p_id = post_id
        self.user = user


class Subscription(Base):
    __tablename__ = "subscriptions"
    sub_id = Column(Integer, primary_key=True)
    #subscriber_id = Column(Integer,ForeignKey('users.userID'))
    subscription_id = Column(Integer, ForeignKey('users.userID'))
    #subscriber = relationship('User')
    subscription = relationship('User')

    def __init__(self,  subscription_id) -> None:
        #self.subscriber = subscriber
        self.subscription_id = subscription_id


class Subscriber(Base):
    __tablename__ = "subscribers"
    sub_id = Column(Integer, primary_key=True)
    subscriber_id = Column(Integer, ForeignKey('users.userID'))

    def __init__(self,  subscriber_id) -> None:
        self.sub_id = subscriber_id


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

#init_db()
#u = User('Goshan', 'admin@ocalhost.ru', "34ggq32q")
#db_session.add(u)
# db_session.commit()

