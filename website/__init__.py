from flask import Flask, session
#database setup
from flask_sqlalchemy import SQLAlchemy
from os import path,urandom
#wichtig fuer login_requirred
from flask_login import LoginManager
#for session
from datetime import timedelta

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] =urandom(42) #random key->make better
    #db setup
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #safe files
    app.config['MUSIC_UPLOAD']='/home/bert/PycharmProjects/flask/music_player/website/static/music/'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024#max file size(50mb)
    app.config['MAX_MUSIC_LENGTH'] = 20 * 1024 * 1024#max file size(20mb)
    app.permanent_session_lifetime = timedelta(hours=1)
    db.init_app(app)

    #register Blueprints
    from .views import views
    from .auth import auth
    from .admin import admin
    from .user_site import user_site
    from .file_sys import file_sys

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
    app.register_blueprint(admin,url_prefix="/")
    app.register_blueprint(user_site,url_prefix="/")
    app.register_blueprint(file_sys,url_prefix="/")

    #db check
    from .models import User, Note, Music
    create_database(app)

    #flask_login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#database checker
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('create Database!!')
