from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120))

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User(name='%s', email='%s',password='%s')>" % (self.name, self.email, self.password)
        #return '<User %r>' % (self.name)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    author = Column(String(120))
    curretTime = Column(String(10))
    user_id = Column(Integer, ForeignKey(User.id))
    #user = relationship(User, backref=backref('users', lazy='dynamic'))

    def __init__(self, title=None, author=None, user_id=None):
        self.title = title
        self.author = author
        self.user_id = user_id

    def __repr__(self):
        return "<Book(title='%s', author='%s', user_id='%s')>" % (self.title, self.author,self.user_id)

class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    desc = Column(String(120))
    time = Column(String(20))

    book_id = Column(Integer, ForeignKey(Book.id))
    #book = relationship(Book, backref=backref('books', lazy='dynamic'))

    user_id = Column(Integer, ForeignKey(User.id))
    #user = relationship(User, backref=backref('users', lazy='dynamic'))

    def __init__(self, desc=None, time=None, book_id=None, user_id=None):
        self.desk = desc
        self.time = time
        self.book_id = book_id
        self.user_id = user_id

    def __repr__(self):
        return "<Bookmark(desc='%s', time='%s', book_id='%s', user_id='%s')>" % (self.desc, self.time,self.book_id,self.user_id)

class BookUser(Base):
    __tablename__ = 'joint'
    id = Column(Integer, primary_key=True)
    currentTime = Column(Integer)

    user_id = Column(Integer, ForeignKey(User.id))
    #user = relationship(User, backref=backref('users', lazy='dynamic'))

    book_id = Column(Integer, ForeignKey(Book.id))
    #book = relationship(Book, backref=backref('books', lazy='dynamic'))

    def __init__(self,currentTime = None):
        self.currentTime = currentTime

    def __repr__(self):
        return "<Joint(currentTime='%s')>" % (self.currentTime)
