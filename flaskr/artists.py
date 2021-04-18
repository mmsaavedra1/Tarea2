from flask import (Flask, g, request, Blueprint, jsonify)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from base64 import b64encode
import sqlite3


bp = Blueprint('artists', __name__)

def codificar_id(name):
    encoded = b64encode(name.encode()).decode('utf-8')
    return encoded[:22]

@bp.route('/artists', methods=['POST'])
def index():
    if request.method ==  'POST':
        # Comprueba que el body está bien hecho
        try:
            name = str(request.form['name'])
        except:
            resp = jsonify({
                'error': f"Input inválido en parámetro 'name'",
            })
            resp.status_code = 400
            return resp
        try:
            age = int(request.form['age'])
        except:
            resp = jsonify({
                'error': f"Input inválido en parámetro 'age'",
            })
            resp.status_code = 400
            return resp

        # Si esta bien hecho continua aca
        # params
        id_ = b64encode(name.encode()).decode('utf-8')[:22]
        albums_url = f'/artists/{id_}/albums'
        tracks_url = f'/artists/{id_}/tracks'
        self_ = f'/artists/{id_}'

        # Objeto respuesta
        resp = jsonify({
                'id': id_,
                'name': name,
                'age': age,
                'albums': albums_url,
                'tracks': tracks_url,
                'self': self_
            })

        # Intenta crear el objeto
        db = get_db()
        try:
            post = db.execute(
                'INSERT INTO Artista (id, name, age, albums, tracks, self)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (id_, name, age, albums_url, tracks_url, self_)
            )
            db.commit()

            # Significa que retorno con exito
            resp.status_code = 200
            return resp

        except sqlite3.IntegrityError as err:
                # Significa que ya existe en BD
            resp.status_code = 409
            return resp
    return 

@bp.route('/artists/<string:artist_id>/albums', methods=['POST'])
def artist_artistId_albums(artist_id):
    if request.method == 'POST':
        # Cromprueba si el body está bien hecho
        try:
            name = str(request.form['name'])
        except:
            resp = jsonify({
                'error': f"Input inválido en parámetro 'name'",
            })
            resp.status_code = 400
            return resp
        
        try:
            genre = str(request.form['genre'])
        except:
            resp = jsonify({
                'error': f"Input inválido en parámetro 'genre'",
            })
            resp.status_code = 400
            return resp
        
        # Si está bien hecho continua aca
        db = get_db()
        try:
             # params
            id_ = b64encode(name.encode()).decode('utf-8')[:22]
            artist_url = f'/artists/{artist_id}'
            tracks_url = f'/albums/{id_}/tracks'
            self_ = f'/albums/{id_}'
            # response
            resp = jsonify({
                'id': id_,
                'artist_id': artist_id,
                'name': name,
                'genre': genre,
                'artist': artist_url,
                'tracks': tracks_url,
                'self': self_
            })

            post = db.execute(
                'INSERT INTO Album (id, artist_id, name, genre, artist, tracks, self)'
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (id_, artist_id, name, genre, artist_url, tracks_url, self_) 
            )
            db.commit()

            # Significa que retorno con exito
            resp.status_code = 200
            return resp

        except sqlite3.IntegrityError as err:
                # Significa que ya existe en BD
            resp.status_code = 409
            return resp


@bp.route('/artists/<string:album_id>/tracks', methods=['POST'])
def artist_albumId_tracks(album_id):
    if request.method == 'POST':
        # Cromprueba si el body está bien hecho
        try:
            name = str(request.form['name'])
        except:
            resp = jsonify({
                'error': f"Input inválido en parámetro 'name'",
            })
            resp.status_code = 400
            return resp
        
        try:
            duration = float(request.form['duration'])
        except:
            resp = jsonify({
                'error': f"Input inválido en parámetro 'duration'",
            })
            resp.status_code = 400
            return resp
        
        # Si está bien hecho continua aca
        db = get_db()
        try:
            # params
            id_ = b64encode(name.encode()).decode('utf-8')[:22]
            query_artist_id = db.execute(f"SELECT artist_id FROM Album WHERE id='{album_id}'").fetchone()[0]
            artist_url = f'/artists/{query_artist_id}'
            album_url = f'/albums/{album_id}'
            self_ = f'/tracks/{id_}'
            # response
            resp = jsonify({
                'id': id_,
                'album_id': album_id,
                'name': name,
                'duration': duration,
                'times_played': 0,
                'artist': artist_url,
                'album': album_url,
                'self': self_
            })

            post = db.execute(
                'INSERT INTO Cancion (id, album_id, name, duration, times_played, artist, album, self)'
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (id_, album_id, name, duration, 0, artist_url, album_url, self_) 
            )
            db.commit()

            # Significa que retorno con exito
            resp.status_code = 200
            return resp

        except sqlite3.IntegrityError as err:
                # Significa que ya existe en BD
            resp.status_code = 409
            return resp

    


