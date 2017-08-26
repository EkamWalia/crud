from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

application = Flask(__name__)
application.config.from_object('config')
application.secret_key = "9999"

application.config["TESTING"] = False
application.config["LOGIN_DISABLED"] = False
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Instance of the database
db = SQLAlchemy(application)
# flask-login config
login_manager = LoginManager()
login_manager.init_app(application)


from app import views,models
