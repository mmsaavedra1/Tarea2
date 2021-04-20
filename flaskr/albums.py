from flask import (Flask, g, request, Blueprint, jsonify)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from base64 import b64encode
import sqlite3
import json


bp = Blueprint('albums', __name__)


def codificar_id(name):
    encoded = b64encode(name.encode()).decode('utf-8')
    return encoded[:22]


@bp.route('/albums', methods=['GET'])
def albums():
    if request.method == 'GET':
        # Intenta crear el objeto
        db = get_db()

        # Se guardan los resultados
        resultado = []
        
        # Se crea la consulta
        get = db.execute(
            'SELECT * FROM Album'
        )

        for row in get.fetchall():
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


@bp.route('/albums/<string:album_id>/tracks', methods=['POST', 'GET'])
def albums_albumId_tracks(album_id):
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
    
    elif request.method == 'GET':
        # Intenta crear el objeto
        db = get_db()
        # Se crea la query
        get = db.execute(
            f"SELECT * FROM Cancion WHERE album_id='{album_id}'"
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
                'error': 'Album no encontrado.'
            })
            resp.status_code = 404
            return resp

   

@bp.route('/albums/<string:album_id>', methods=['GET', 'DELETE'])
def albums_artistId(album_id):
    if request.method == 'GET':
        # Intenta crear el objeto
        db = get_db()
        # Se crea la query
        row = db.execute(
            f"SELECT * FROM Album WHERE id='{album_id}'"
        ).fetchone()
        if row:
            resp = jsonify({
                'id': row[0],
                'artist_id': row[1],
                'name': row[2],
                'genre': row[3],
                'artist': row[4],
                'tracks': row[5],
                'self': row[6]
            })
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({
                'error': 'Album no encontrado.'
            })
            resp.status_code = 404
            return resp

    elif request.method == 'DELETE':
        # Intenta crear el objeto
        db = get_db()
        # Se crea la query
        row = db.execute(
            f"SELECT * FROM Album WHERE id='{album_id}'"
        ).fetchone()
        if row:
            pragma = db.execute(
                'PRAGMA foreign_keys = ON;'
            )
            row = db.execute(
                f"DELETE FROM Album WHERE id='{album_id}'"
            )
            db.commit()
            resp = jsonify({
                'description': 'Album eliminado.'
            })
            resp.status_code = 204
            return resp
        else:
            resp = jsonify({
                'error': 'Album inexistente.'
            })
            resp.status_code = 404
            return resp
    
