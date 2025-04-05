from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.auth import auth as auth_blueprint
    from app.admin import admin as admin_blueprint
    from app.main import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(main_blueprint)

    return app