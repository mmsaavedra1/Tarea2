from flask import (Flask, g, request, Blueprint, jsonify)
from werkzeug.exceptions import abort
import sqlite3
import json
import os

from Tarea2.extensions import db
from sqlalchemy import text
from Tarea2.models import *

canciones = Blueprint('canciones', __name__)



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
        row = db.session.query(Cancion).filter(Cancion.id == track_id).all()

        if row:
            resp = jsonify({
                'id': row[0].id,
                'album_id': row[0].album_id,
                'name': row[0].name,
                'duration': row[0].duration,
                'times_played': row[0].times_played,
                'artist': row[0].artist,
                'album': row[0].album,
                'self': row[0].self_
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
        tracks = db.session.query(Cancion).filter(Cancion.id == track_id).all()
        if tracks:
            for track in tracks:
                value = track.times_played + 1
                setattr(track, times_played, value)
                db.session.commit()
            # Retorna exito
            resp.status_code = 200
        else:
            # Retorna que no existe el id de la URL
            resp.status_code = 404
    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp