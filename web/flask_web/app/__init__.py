from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app) # сама база данных
migrate = Migrate(app, db) # механизм миграции

login = LoginManager(app) # работа с пользователем
login.login_view = 'login' # не дает пользователю перейти на /login, пока его нет в системе

bootstrap = Bootstrap(app)

from app import routes, models






