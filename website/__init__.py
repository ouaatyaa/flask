from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key='1c0055688a0dbdb4332a1dac23ce52fb'

#             Databases
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
#          session login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # indicate the login route in case:  @login_required
login_manager.login_message_category = 'info' #for Alert msgs in info boostrp info styl

 
from website import routes
