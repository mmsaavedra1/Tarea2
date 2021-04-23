from flask import (Flask, g, request, Blueprint, jsonify)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from base64 import b64encode
import sqlite3
import json
import os


bp = Blueprint('artists', __name__)

def codificar_id(name):
    encoded = b64encode(name.encode()).decode('utf-8')
    return encoded[:22]


@bp.route('/artists', methods=['GET', 'POST'])
def artists():
    if request.method ==  'POST':

        # Comprueba que el body está bien hecho
        if ( len(request.form) == 0) or (name == None) or (age == None):
            resp = jsonify({
                    'error': f"Input invalido"
                })
            resp.status_code = 400

            return resp
        
        

        try:
            name = int(name)
        except:
            resp = jsonify({
                    'error': f"Input invalido",
                    'TIPO': f"{type(age)}"
                })
            resp.status_code = 400

            return resp

        # Si esta bien hecho continua aca
        # params
        id_ = b64encode(name.encode()).decode('utf-8')[:22]
        albums_url = f'{os.environ.get("HEROKU_URL")}artists/{id_}/albums'
        tracks_url = f'{os.environ.get("HEROKU_URL")}artists/{id_}/tracks'
        self_ = f'{os.environ.get("HEROKU_URL")}artists/{id_}'

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
            resp.status_code = 201
            return resp

        except sqlite3.IntegrityError as err:
                # Significa que ya existe en BD
            resp.status_code = 409
            return resp

    elif request.method == 'GET':
        # Intenta crear el objeto
        db = get_db()

        # Se guardan los resultados
        resultado = []
        
        # Se crea la consulta
        get = db.execute(
            'SELECT * FROM Artista'
        )

        for row in get.fetchall():
            resultado.append({
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'albums': row[3],
                'tracks': row[4],
                'self': row[5]
            })
        
        resp = jsonify(resultado)
        resp.status_code = 200

        return resp

    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp


@bp.route('/artists/<string:artist_id>/albums', methods=['POST', 'GET'])
def artist_artistId_albums(artist_id):
    if request.method == 'POST':
        # Cromprueba si el body está bien hecho
        if ( len(request.form) == 0) or ("name" not in request.args) or ("genre" not in request.args):
            resp = jsonify({
                    'error': f"Input invalido",
                    'valores': request.data
                })
            resp.status_code = 400

            return resp
        
        name = request.form.get("name")
        genre = request.form.get("genre")

        try:
            name = str(name)
            genre = str(genre)
        except:
            resp = jsonify({
                    'error': f"Input invalido"
                })
            resp.status_code = 400

            return resp
        
        # Si está bien hecho continua aca
        db = get_db()
        # Comrprobar que el artista existe para crear un album
        query = db.execute(
            f"SELECT * FROM Artista WHERE id='{artist_id}'"
        ).fetchone()
        if query:
            try:
                # params
                id_ = b64encode(name.encode()).decode('utf-8')[:22]
                artist_url = f'{os.environ.get("HEROKU_URL")}artists/{artist_id}'
                tracks_url = f'{os.environ.get("HEROKU_URL")}albums/{id_}/tracks'
                self_ = f'{os.environ.get("HEROKU_URL")}albums/{id_}'
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
                resp.status_code = 201
                return resp

            except sqlite3.IntegrityError as err:
                    # Significa que ya existe en BD
                resp.status_code = 409
                return resp
        else:
            resp = jsonify({
                'error': 'Artista no existente.'
            })
            resp.status_code = 422
            return resp

    elif request.method == 'GET':
        # Intenta crear el objeto
        db = get_db()
        # Se crea la query
        get = db.execute(
            f"SELECT * FROM Album WHERE artist_id='{artist_id}'"
        ).fetchall()
        if get:
            resultado = []
            for row in get:
                resultado.append({
                    'id': row[0],
                    'artist_id': row[1],
                    'name': row[2],
                    'genre': row[3],
                    'artist': row[4],
                    'tracks': row[5],
                    'self': row[6]
                })
            
            resp = jsonify(resultado)
            resp.status_code = 200

            return resp
        else:
            resp = jsonify({
                'error': 'Artista no encontrado.'
            })
            resp.status_code = 404
            return resp

    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp


@bp.route('/artists/<string:artist_id>/tracks', methods=['GET'])
def artist_artistId_tracks(artist_id):
    if request.method == 'GET':
        # Intenta crear el objeto
        db = get_db()
        # Se crea la query
        get = db.execute(
            f"SELECT * FROM Cancion WHERE artist='/artists/{artist_id}'"
        ).fetchall()
        if get:
            resultado = []
            for row in get:
                resultado.append({
                    'id': row[0],
                    'album_id': row[1],
                    'name': row[2],
                    'duration': row[3],
                    'times_played': row[4],
                    'artist': row[5],
                    'album': row[6],
                    'self': row[7]
                })
            
            resp = jsonify(resultado)
            resp.status_code = 200

            return resp
        else:
            resp = jsonify({
                'error': 'Artista no encontrado.'
            })
            resp.status_code = 404
            return resp

    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp




@bp.route('/artists/<string:artist_id>', methods=['GET', 'DELETE'])
def artist_artistId(artist_id):
    if request.method == 'GET':
        # Intenta crear el objeto
        db = get_db()
        # Se crea la query
        row = db.execute(
            f"SELECT * FROM Artista WHERE id='{artist_id}'"
        ).fetchone()
        if row:
            resp = jsonify({
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'albums': row[3],
                'tracks': row[4],
                'self': row[5]
            })
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({
                'error': 'Artista no encontrado.'
            })
            resp.status_code = 404
            return resp

    elif request.method == 'DELETE':
        # Intenta crear el objeto
        db = get_db()
        # Se crea la query
        row = db.execute(
            f"SELECT * FROM Artista WHERE id='{artist_id}'"
        ).fetchone()
        if row:
            pragma = db.execute(
                'PRAGMA foreign_keys = ON;'
            )
            row = db.execute(
                f"DELETE FROM Artista WHERE id='{artist_id}'"
            )
            db.commit()
            resp = jsonify({
                'description': 'Artista eliminado.'
            })
            resp.status_code = 204
            return resp
        else:
            resp = jsonify({
                'error': 'Artista inexistente.'
            })
            resp.status_code = 404
            return resp
    
    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp
        
@bp.route('/artists/<string:artist_id>/albums/play')
def artist_artistId_albums_play(artist_id):
    if request.method == 'POST':
        pass
        #TODO
    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp
