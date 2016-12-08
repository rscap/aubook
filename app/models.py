from app import db
import datetime
#from sqlalchemy import ForeignKey
#from sqlalchemy.orm import relationship

# BookUser = db.Table('bookUsers',
#   db.Column('id', db.Integer, primary_key=True),
#   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#   db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
#   db.Column('currentTime', db.Float)
# )

class BookUser(db.Model):
    __tablename__ = 'book_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    currentTime = db.Column(db.Float)


class User(db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    #books = db.relationship('Book', secondary=BookUser, backref=db.backref('books')) #, lazy='dynamic')
    books = db.relationship('Book', secondary='book_users', backref=db.backref('books')) #, lazy='dynamic')


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return "<User(name='%s', email='%s',password='%s')>" % (self.name, self.email, self.password)


class Book(db.Model):
    #__tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    author = db.Column(db.String(120))
    #curretTime = Column(String(10))
    #user_id = Column(Integer, ForeignKey(User.id))
    #user = relationship("User" secondary=BookUser, backref='users')

    def __init__(self, title=None, author=None):
        self.title = title
        self.author = author
        #self.user_id = user_id

    def __repr__(self):
        return "<Book(title='%s', author='%s')>" % (self.title, self.author)

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(120))
    time = db.Column(db.String(20))
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id), index=True)
    #book = relationship(Book, backref=backref('books', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id),index=True)
    #user = relationship(User, backref=backref('users', lazy='dynamic'))

    def __init__(self, desc=None, time=None, book_id=None, user_id=None):
        self.desc = desc
        self.time = time
        self.book_id = book_id
        self.user_id = user_id

    def __repr__(self):
        return "<Bookmark(desc='%s', time='%s', book_id='%s', user_id='%s')>" % (self.desc, self.time,self.book_id,self.user_id)
