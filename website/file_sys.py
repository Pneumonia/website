from flask import Flask, render_template, json, jsonify, Blueprint, request, redirect, flash, url_for, current_app, \
    Response
from flask_login import current_user, login_required
from .models import Note, User, Music
from werkzeug.utils import secure_filename
import os
from . import db
import logging
from pydub import AudioSegment, generators
from pydub.playback import play, _play_with_simpleaudio
import simpleaudio
import json

file_sys = Blueprint("file_sys", __name__)

def music_refresh():
    music_files = os.listdir("/home/bert/PycharmProjects/flask/music_player/website/static/music/")
    # alte loeschen
    title_exist = Music.query.order_by(Music.id).all()
    title_exist = [music.title for music in title_exist]
    if len(music_files) < len(title_exist):
        for item in title_exist:
            if item not in music_files:
                no_title = Music.query.filter_by(title=item).first()
                flash(no_title.title + " was not found and deleted!", category="success")
                db.session.delete(no_title)
                db.session.commit()
    # neue einträge
    for item in music_files:
        title, link = item, "/home/bert/PycharmProjects/flask/music_player/website/static/music/" + item
        music = Music.query.filter_by(title=title).first()
        if not music:
            new_music = Music(title=title, link=link)
            db.session.add(new_music)
            db.session.commit()
            flash(title + " wurde importiert", category="success")
    flash("music was refresched!", category="success")
    return redirect(url_for("file_sys.music_player"))

def allowed_music_filesize(filesize):
    if int(filesize) <= current_app.config['MAX_MUSIC_LENGTH']:
        return True
    else:
        return False

@file_sys.route("/upload-music", methods=["GET", "POST"])
@login_required
def upload():
    valid_musicfile = ["MP3", "AAC", "M4A", "WMA", "FLAC", "ALAC", "WAV", "AIFF", "PCM", "OGG"]
    if request.method == "POST":
        if request.files["music"]:
            music = request.files["music"]
            if music.filename != "":
                if music.filename.upper().split(".")[1] in valid_musicfile:
                    if "filesize" in request.cookies:
                        if allowed_music_filesize(request.cookies["filesize"]):
                            sec_filename = secure_filename(music.filename)  # name securt
                            music.save(os.path.join(current_app.config['MUSIC_UPLOAD'],
                                                    sec_filename))  # currnt_app und auf __init__zuzugreifen
                            flash("music file Uploaded!", category="success")
                            music_refresh()
                            return redirect(request.url)  # back to start
                        else:
                            flash("file to big", category="error")
                    else:
                        flash("no filesize detected", category="error")
                else:
                    flash("not a alowed file " + "alowed files: " + ", ".join(valid_musicfile), category="error")
            else:
                flash("file has no name", category="error")
        else:
            flash("not a music file, music was not Uploaded!", category="error")
    return render_template("upload.html", user=current_user)

safe = []

def safe_change(wert):
    global safe
    safe = wert

@file_sys.route('/music_player', methods=["GET", "POST"])
@login_required
def music_player():
    music_refresh()
    if request.method == "POST":
        play = request.form.get("play_music")
        if play:
            play = Music.query.filter_by(id=play).first()
            play = "music/"+play.title
            return render_template("music_player.html", user=current_user, entries=Music.query.all(),play=play)

        music = request.form.get("music")
        print("\nmusic_tell",music,"\n")
        stop = request.form.get("stop")
        music = Music.query.filter_by(id=music).first()
        if stop and len(safe) > 0:
            try:
                safe[0].stop()
                flash("lied angehalten!", category="success")
            except:
                flash("ERROR!!!", category="error")
        if music:
            if len(safe) > 0:
                try:
                    safe[0].stop()
                    flash("neus lied: " + music.title, category="success")
                except:
                    flash("ERROR!!", category="error")
            playback = AudioSegment.from_file(music.link)
            playback = _play_with_simpleaudio(playback)
            safe_change([playback])
    return render_template("music_player.html", user=current_user, entries=Music.query.all(),play=None)

@file_sys.route("/delete-music" , methods=["POST"])#methods=["DELETE","PUT"]
@login_required
def delete_music():
    music = json.loads(request.data)
    musicId = music['musicId']
    music = Music.query.get(musicId)
    if music:
        title = music.title
        try:
            os.system("rm -f "+music.link)
            flash(music.title+ " was deleted",category="success")
        except:
            flash(music.title+" wasen't deleted",category="error")
        db.session.delete(music)
        db.session.commit()
        music_refresh()
    return jsonify({})


@file_sys.route("/static/music/<string:name>",methods=["POST","GET"])
@login_required
def play(name):
    name = "/home/bert/PycharmProjects/flask/music_player/website/static/music/"+name
    print("\nmusic_play",name,"\n")
    def generator(name):
        count=1
        with open(name,"rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
                logging.debug('Music data fragment : ' + str(count))
                count += 1
    return Response(generator(name), mimetype="audio/mp3")
