from flask import Blueprint, render_template, request, flash, redirect, url_for,session
#db imports
from . import db
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash #no inverse
#einfache variante  um navbar sowie page erreichbarkeit für an und abgemeldet zu bearbeiten
from flask_login import login_user, login_required, logout_user, current_user#geht nur wenn in models. UserMixin verwendet wird

auth = Blueprint("auth", __name__)

@auth.route("/login" , methods=["GET","POST"])#handle POST request
def login():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()#erste übereinstimmung
        if user:
            if check_password_hash(user.password,password):#hash gespeichertes pw gegen pw
                flash(f"login successfully, hello {user.first_name}", category="success")
                login_user(user, remember=True)#user angemeldet und beibehalten das logt
                #session
                session.permanent = True  # session ist permanent
                session["user"] = user.first_name
                return redirect(url_for("views.home"))
            else:
                flash("incorrect password!", category="error")
        else:
            flash("Email does not exist",category="error")
    return render_template("login.html",user=current_user)

@auth.route("/logout")
@login_required #kann nur bei login genutzt werden
def logout():
    name = current_user.first_name #first name auch in current_user
    session.pop("user", None)
    logout_user()#loggt current user aus
    flash(f"by by {name}!", category="success")
    return redirect(url_for("auth.login"))

@auth.route("/sign_up", methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")#aus input in form
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user= User.query.filter_by(email=email).first()
        if user:
            flash("email allready in use!", category="error" )
        elif len(email) < 4:
            flash("Email is to short (must be greater than 4 char)", category="error")#msg in unt farbe
            pass
        elif len(first_name) < 2:
            flash("first name must be greater than 2 Char",category="error")
            pass
        elif password1 != password2:
            flash("passwords don\'t match",category="error")
            pass
        elif len(password1) < 3:
            flash("password must be grater than 3 char", category="error")
            pass
        else:
            #new User
            new_user=User(email=email, first_name=first_name,password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created!!", category="success")
            # session
            session.permanent = True
            session["user"] = new_user.first_name
            login_user(new_user, remember=True)
            return redirect(url_for("views.home"))

    return render_template("sign_up.html",user=current_user)

