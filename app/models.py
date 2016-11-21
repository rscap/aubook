from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True)
    author = Column(String(120))

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User, backref=backref('users', lazy='dynamic'))

    def __init__(self, title=None, author=None):
        self.book_title = book_title
        self.book_author = book_author

    def __repr__(self):
        return '<Book %r>' % (self.book_title)

class Bookmark(Base):
    __tablename__ = 'bookmark'
    id = Column(Integer, primary_key=True)
    desc = Column(String(120))
    time = Column(String(20))
    currentTime = Column(Integer)

    book_id = Column(Integer, ForeignKey(Book.id))
    book = relationship(Book, backref=backref('books', lazy='dynamic'))

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User, backref=backref('users', lazy='dynamic'))

    def __init__(self, currentTime=None):
        self.book_title = book_title
        self.book_author = book_author

    def __repr__(self):
        return '<Book %r>' % (self.book_title)
