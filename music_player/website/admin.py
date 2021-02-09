from flask import Blueprint, render_template, request, jsonify, flash,redirect,url_for
from flask_login import login_required, current_user
from . import db  # db name = database.db
from flask_sqlalchemy import SQLAlchemy
from .models import User, Note  # anzeigen aller User
import json

admin = Blueprint("admin", __name__)

@admin.route("/user_list")  # warum ist login by default required
@login_required
def user_list():
    if current_user.id != 1:
        return redirect(url_for("views.home"))
    else:
        return render_template("user_list.html", user=current_user, values_user=User.query.all())

@admin.route('/delete-note-admin', methods=['POST'])  # für note löschen, ' ist wichtig, " sind flasch
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']  # wichtig das noteId
    note = Note.query.get(noteId)
    if note:  # gint es eine not?
        db.session.delete(note)
        db.session.commit()
        flash("note deletet!",category="success")
    return jsonify({})  # empty python dic

@admin.route("/delete-user", methods=['POST'])
@login_required
def delete_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    if user:
        if user.id != current_user.id:#admin löscht sich selber nicht
            if len(user.notes)>0:
                for note in user.notes: # weil die notes nicht mitgelöscht werden
                    db.session.delete(note)
                    db.session.commit()
                    flash("note deletet!", category="success")
            db.session.delete(user)
            db.session.commit()
            flash("user deletet!", category="success")
    return jsonify({})
