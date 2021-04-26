from flask import (Flask, g, request, Blueprint, jsonify)
from werkzeug.exceptions import abort
from base64 import b64encode
import sqlite3
import json
import os

from Tarea2.extensions import db
from sqlalchemy import text
from Tarea2.models import *

canciones = Blueprint('canciones', __name__)


def codificar_id(name):
    encoded = b64encode(name.encode()).decode('utf-8')
    return encoded[:22]


@canciones.route('/tracks', methods=['GET'])
def tracks():
    if request.method == 'GET':
        # Se guardan los resultados
        resultado = []
        
        # Se crea la consulta
        get = db.session.query(Cancion)

        for row in get.all():
            resultado.append({
                'id': row.id,
                'album_id': row.album_id,
                'name': row.name,
                'duration': row.duration,
                'times_played': row.times_played,
                'artist': row.artist,
                'album': row.album,
                'self': row.self_
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


@canciones.route('/tracks/<string:track_id>', methods=['GET', 'DELETE'])
def tracks_trackId(track_id):
    if request.method == 'GET':
        # Se crea la query
        row = db.session.query(Cancion).filter(Cancion.id == track_id).all()[0]

        if row:
            resp = jsonify({
                'id': row.id,
                'album_id': row.album_id,
                'name': row.name,
                'duration': row.duration,
                'times_played': row.times_played,
                'artist': row.artist,
                'album': row.album,
                'self': row.self_
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
        # Se crea la query
        result = db.session.query(Cancion).filter(Cancion.id == track_id).all()

        if result:
            db.session.delete(result[0])
            db.session.commit()
            
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


@canciones.route('/tracks/<string:track_id>/play')
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