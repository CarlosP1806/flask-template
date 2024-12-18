from flask import (
    Blueprint, request, jsonify 
)
from api.services.db_service import get_db

bp = Blueprint('song', __name__, url_prefix='/songs')

@bp.route('/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        artist = data.get('artist')
        
        if title is None or artist is None:
            return jsonify({"error": "Missing required information."}), 400

        db = get_db()
        cursor = db.cursor(dictionary=True)

        try: 
            cursor.execute(
                'INSERT INTO song (title, artist) VALUES (%s, %s)',
                (title, artist)
            )
            db.commit()
            cursor.execute('SELECT id, title, artist FROM song WHERE title = %s', (title,))
            new_song = cursor.fetchone()

            return jsonify({"song": new_song}), 201

        except Exception as e:
            if "Duplicate entry" in str(e):
                return jsonify({"error": "Song already exists."}), 400
            
            return jsonify({"error": "An unexpected error occurred."}), 400

    elif request.method == 'GET':
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute('SELECT id, title, artist FROM song')
        songs = cursor.fetchall()

        return jsonify({"songs": songs}), 200 

@bp.route('/<int:song_id>', methods=('GET', 'PUT', 'DELETE'))
def song(song_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute('SELECT id, title, artist FROM song WHERE id = %s', (song_id,))
        song = cursor.fetchone()

        if song is None:
            return jsonify({"error": "Song not found."}), 404

        return jsonify({"song": song}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        title = data.get('title')
        artist = data.get('artist')

        if title is None or artist is None:
            return jsonify({"error": "Missing required information."}), 400

        try:
            cursor.execute(
                'UPDATE song SET title = %s, artist = %s WHERE id = %s',
                (title, artist, song_id)
            )
            db.commit()

            cursor.execute('SELECT id, title, artist FROM song WHERE id = %s', (song_id,))
            updated_song = cursor.fetchone()

            return jsonify({"song": updated_song}), 200

        except Exception as e:
            if "Duplicate entry" in str(e):
                return jsonify({"error": "Song already exists."}), 400

            return jsonify({"error": "An unexpected error occurred."}), 400

    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM song WHERE id = %s', (song_id,))
        db.commit()

        return jsonify({"message": "Song deleted."}), 200
    