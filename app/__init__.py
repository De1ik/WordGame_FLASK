from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, LoginManager

from config import *


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in before using this page'

# Тут можно выполнять дополнительные настройки приложения, если это необходимо.

# Импортируем модули представлений и модели, чтобы они стали известны приложению
from . import routes
from . import models
from . import wtf_forms

