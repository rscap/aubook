from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120))
    #book = relationship("Book", secondary=BookUser, back_ref='User')

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User(name='%s', email='%s',password='%s')>" % (self.name, self.email, self.password)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    author = Column(String(120))
    #curretTime = Column(String(10))
    #user_id = Column(Integer, ForeignKey(User.id))
    #user = relationship("User" secondary=BookUser, backref='users')

    def __init__(self, title=None, author=None):
        self.title = title
        self.author = author
        #self.user_id = user_id

    def __repr__(self):
        return "<Book(title='%s', author='%s')>" % (self.title, self.author)

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
    __tablename__ = 'BookUser'
    id = Column(Integer, primary_key=True)
    currentTime = Column(String(10))
    user_id = Column(Integer, ForeignKey(User.id))
    book_id = Column(Integer, ForeignKey(Book.id))
    #user = relationship(User, backref=backref('users', lazy='dynamic'))
    #book = relationship(Book, backref=backref('books', lazy='dynamic'))

    def __init__(self,currentTime = None, user_id=None, book_id=None):
        self.currentTime = currentTime
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return "<BookUser(currentTime='%s', user_id='%s',book_id='%s')>" % (self.currentTime,self.user_id,self.book_id)
