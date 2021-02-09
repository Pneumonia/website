from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db #db name = database.db
from flask_sqlalchemy import SQLAlchemy
from .models import User, Note #anzeigen aller User

user_site = Blueprint("user_site", __name__)

@user_site.route("/user_site")
def user():
    return render_template("user_site.html",user=current_user)