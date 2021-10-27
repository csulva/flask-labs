from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from blogger import app
from werkzeug.security import check_password_hash, generate_password_hash
from . import login_manager

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(50), unique=True, index=True)
    dateofreg = db.Column(db.DateTime, default=datetime.datetime.now)

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Cannot display password.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, firstname, lastname, username, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email


class Post(db.Model):
    __tablename__ = 'posts'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    puid = db.Column(db.Integer, db.ForeignKey('users.uid'))

    def __init__(self, title, description, puid):
        self.title = title
        self.description = description
        self.puid = puid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.create_all()
