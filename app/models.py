from sqlalchemy.orm import validates
from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    team = db.relationship('Teams', backref='author', lazy='dynamic')
    todo = db.relationship('Todo', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(75), nullable=False)
    abbr = db.Column(db.String(3), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    __table_args__ = (db.UniqueConstraint('user_id', 'abbr', name='team_name'),
                 )



    def __repr__(self):
        return '<Teams {}>'.format(self.team)

    @validates('team', 'abbr')
    def convert_upper(self, key, value):
        return value.upper()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(75), nullable=False)
    desc = db.Column(db.String(150), nullable=True)
    mc_number = db.Column(db.Integer)
    dnc_doc = db.Column(db.String(50), nullable=True)
    prog_edit = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    fal = db.Column(db.String(50), nullable=True)     
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    __table_args__ = (db.UniqueConstraint('user_id', 'todo', name='todo_name'),
                 )

    def __repr__(self):
        return '<Todo {}>'.format(self.todo)



