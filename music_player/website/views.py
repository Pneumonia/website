#route
from flask import Blueprint, render_template,request,flash , jsonify,session
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint("views", __name__)#kind of class



@views.route("/",methods=["POST","GET"])
@login_required
def home():
    if request.method == "POST":#sicher
        note = request.form.get("note")
        if len(note) <1:
            flash("note to short",category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id) #note hinzufügen
            db.session.add(new_note)
            db.session.commit()
            flash("Note added ",category="success")
    return render_template("home.html", user=current_user,values_user=User.query.all())#an alle html die extends base haben muss user gegeben werden



@views.route('/delete-note', methods=["POST"])#für note löschen, ' ist wichtig, " sind flasch
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']#wichtig das noteId
    note = Note.query.get(noteId)
    if note:#gint es eine not?
        if note.user_id == current_user.id:#ist die note von dem user?
            db.session.delete(note)
            db.session.commit()
            flash("note deletet!", category="success")
    return jsonify({})#empty python dic
