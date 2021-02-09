from . import db  # . ist current package/ . ist wie website was man nimmt wenn man nicht im verzeichniss ist
from flask_login import UserMixin
from sqlalchemy.sql import func #um bei jeder neuen Note direkt das datum zu adden
import simpleaudio

#aussehen db
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) #db.Column(TYPE of information)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())#adds date to Note
    #foreign key, schlüsser zur ID anderer db.Column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#id von bestehenden User
                                                            #id aus User

class User(db.Model,UserMixin):#mutter ist db.Model und UserMixin #Blueprint fuer User daten
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True)#max len string 150
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')#list of all notes of specific User

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),unique=True)
    link = db.Column(db.String(150))









