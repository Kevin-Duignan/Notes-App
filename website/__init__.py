from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DATABASE = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "HELLO"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    with app.app_context():
        db.create_all()

    # Manage logged in user
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Once logged in load the user by primary key (id)
    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app
