from app import db
import datetime

class BookUser(db.Model):
    __tablename__ = 'book_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    currentTime = db.Column(db.Float, default=0.0)

    def __init__(self,user_id,book_id,currentTime):
        self.user_id = user_id
        self.book_id = book_id
        self.currentTime = currentTime

    def __repr__(self):
        return "<BookUser(user_id='%s',book_id='%s',currentTime='%s')>" % (self.user_id,self.book_id,self.currentTime)


class User(db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), nullable=False)
    #books = db.relationship('Book', secondary=BookUser, backref=db.backref('books')) #, lazy='dynamic')
    books = db.relationship('Book', secondary='book_users', backref=db.backref('books')) #, lazy='dynamic')


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User(name='%s', email='%s',password='%s')>" % (self.name, self.email, self.password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Book(db.Model):
    #__tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    shareable = db.Column(db.Boolean, nullable=False)
    #curretTime = Column(String(10))
    #user_id = Column(Integer, ForeignKey(User.id))
    #user = relationship("User" secondary=BookUser, backref='users')

    def __init__(self, title=None, author=None, shareable=True):
        self.title = title
        self.author = author
        self.sharable = shareable
        #self.user_id = user_id

    def __repr__(self):
        return "<Book(title='%s', author='%s',shareable='%s')>" % (self.title, self.author, self.shareable)

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(240))
    time = db.Column(db.Float)
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

    def seralize(self):
        return {
            'id':self.id,
            'desc': self.desc,
            'time': self.time,
            'book_id': self.book_id,
            'user_id': self.user_id,
        }

class PWReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reset_key = db.Column(db.String(128), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetime = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    user = db.relationship(User, lazy='joined')
    has_activated = db.Column(db.Boolean, default=False)
