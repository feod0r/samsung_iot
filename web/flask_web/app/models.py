from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # не поле, а тим взаимоотношения с таблицей Post
    posts = db.relationship('Post', backref='author', lazy='dynamic') # backref - имя поля FK, 

    def __repr__(self): # сообщает Python, как печатать объекты этого класса
        return '<User {}>'.format(self.username)

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)


@login.user_loader # Пользовательский загрузчик
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user - имя таблицы

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class BD_coordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sat_lat = db.Column(db.Float, index=True)
    sat_long = db.Column(db.Float, index=True)
    sat_height = db.Column(db.Float, index=True)
    ant_lat = db.Column(db.Float, index=True)
    ant_long = db.Column(db.Float, index=True)
    ant_height = db.Column(db.Float, index=True)
    teta = db.Column(db.Integer, index=True)
    fi_priv = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)






