from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, LoginManager
from flask_migrate import Migrate
from flask_caching import Cache

from config import *


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['CASHE_TYPE'] = 'simple'
cashe = Cache(app)


from applications.views.blueprint_wordle.wordle_modes import wordle_index, wordle_5_lt_bp, wordle_6_lt_bp, wordle_7_lt_bp
app.register_blueprint(wordle_index)
app.register_blueprint(wordle_7_lt_bp, url_prefix='/games/wordle')
app.register_blueprint(wordle_6_lt_bp, url_prefix='/games/wordle')
app.register_blueprint(wordle_5_lt_bp, url_prefix='/games/wordle')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in before using this page'


from . import routes
from . import models
from . import wtf_forms

