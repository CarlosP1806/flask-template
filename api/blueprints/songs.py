from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from api.models import Song
from api.services.db_service import db_session

bp = Blueprint('song', __name__, url_prefix='/songs')

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        artist = data.get('artist')

        if not title or not artist:
            return jsonify({"error": "Missing required information."}), 400

        new_song = Song(title=title, artist=artist)
        try:
            db_session.add(new_song)
            db_session.commit()
            return jsonify({"song": {"id": new_song.id, "title": new_song.title, "artist": new_song.artist}}), 201
        except IntegrityError:
            db_session.rollback()
            return jsonify({"error": "Song already exists."}), 400
        except Exception:
            db_session.rollback()
            return jsonify({"error": "An unexpected error occurred."}), 400

    elif request.method == 'GET':
        songs = db_session.query(Song).all()
        return jsonify({"songs": [{"id": song.id, "title": song.title, "artist": song.artist} for song in songs]}), 200

@bp.route('/<int:id>', methods=('GET', 'PUT', 'DELETE'))
def song(id):
    song = db_session.query(Song).get(id)

    if not song:
        return jsonify({"error": "Song not found."}), 404

    if request.method == 'GET':
        return jsonify({"song": {"id": song.id, "title": song.title, "artist": song.artist}}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        title = data.get('title') or song.title
        artist = data.get('artist') or song.artist

        song.title = title
        song.artist = artist
        try:
            db_session.commit()
            return jsonify({"song": {"id": song.id, "title": song.title, "artist": song.artist}}), 200
        except Exception:
            db_session.rollback()
            return jsonify({"error": "An unexpected error occurred."}), 400

    elif request.method == 'DELETE':
        db_session.delete(song)
        db_session.commit()
        return jsonify({"message": "Song deleted."}), 200
