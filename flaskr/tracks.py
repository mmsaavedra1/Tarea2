from flask import (Flask, g, request, Blueprint, jsonify)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from base64 import b64encode
import sqlite3
import json


bp = Blueprint('tracks', __name__)


def codificar_id(name):
    encoded = b64encode(name.encode()).decode('utf-8')
    return encoded[:22]


@bp.route('/tracks', methods=['GET'])
def tracks():
    if request.method == 'GET':
        # Intenta crear el objeto
        db = get_db()

        # Se guardan los resultados
        resultado = []
        
        # Se crea la consulta
        get = db.execute(
            'SELECT * FROM Cancion'
        )

        for row in get.fetchall():
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
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp

@bp.route('/tracks/<string:track_id>', methods=['GET'])
def tracks_trackId(track_id):
    if request.method == 'GET':
         # Intenta crear el objeto
        db = get_db()
        # Se crea la query
        row = db.execute(
            f"SELECT * FROM Cancion WHERE id='{track_id}'"
        ).fetchone()
        if row:
            resp = jsonify({
                'id': row[0],
                'album_id': row[1],
                'name': row[2],
                'duration': row[3],
                'times_played': row[4],
                'artist': row[5],
                'album': row[6],
                'self': row[7]
            })
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({
                'error': 'Cancion no encontrada.'
            })
            resp.status_code = 404
            return resp
    
    elif request.method == 'DELETE':
        # Intenta crear el objeto
        db = get_db()
        # Se crea la query
        row = db.execute(
            f"SELECT * FROM Cancion WHERE id='{track_id}'"
        ).fetchone()
        if row:
            pragma = db.execute(
                'PRAGMA foreign_keys = ON;'
            )
            row = db.execute(
                f"DELETE FROM Cancion WHERE id='{track_id}'"
            )
            db.commit()
            resp = jsonify({
                'description': 'Cancion eliminada.'
            })
            resp.status_code = 204
            return resp
        else:
            resp = jsonify({
                'error': 'Cancion inexistente.'
            })
            resp.status_code = 404
            return resp
    
    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp


@bp.route('/tracks/<string:track_id>/play')
def tracks_trackId_play(track_id):
    if request.method == 'POST':
        pass
        #TODO
    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp