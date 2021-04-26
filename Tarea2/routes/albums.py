from flask import (Flask, g, request, Blueprint, jsonify)
from werkzeug.exceptions import abort
from base64 import b64encode
import sqlite3
import json
import os

from Tarea2.extensions import db
from sqlalchemy import text
from Tarea2.models import *

albumnes = Blueprint('albumnes', __name__)


@albumnes.route('/albums', methods=['GET'])
def albums():
    if request.method == 'GET':

        # Se guardan los resultados
        resultado = []
        
        # Se crea la consulta
        get = db.session.query(Album)

        for row in get.all():
            resultado.append({
                'id': row.id,
                'artist_id': row.artist_id,
                'name': row.name,
                'genre': row.genre,
                'artist': row.artist,
                'tracks': row.tracks,
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


@albumnes.route('/albums/<string:album_id>/tracks', methods=['POST', 'GET'])
def albums_albumId_tracks(album_id):
    if request.method == 'POST':
        # Comprueba que el body está bien hecho
        valores = request.json
        if ("name" not in valores) or ("duration" not in valores):
            resp = jsonify({
                    'error': f"Input invalido en json",
                })
            resp.status_code = 400

            return resp
        else:
            name = valores["name"]
            duration = valores["duration"]


        # Si está bien hecho continua aca
        query = db.session.query(Album).filter(Album.id == album_id).all()
        
        if query:
            # Body request
            id_ = b64encode(f"{name}:{query[0].id}".encode()).decode('utf-8')[:22]
            artist_url = f'{os.environ.get("HEROKU_URL")}artists/{query[0].id}'
            album_url = f'{os.environ.get("HEROKU_URL")}albums/{album_id}'
            self_ = f'{os.environ.get("HEROKU_URL")}tracks/{id_}'
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
                
            query2 = db.session.query(Cancion).filter(Cancion.id == id_).all()
            if query2:
                # Significa que ya existe en BD
                resp.status_code = 409
                return resp
            else:
                track = Cancion(id_, album_id, name, duration, 0, artist_url, album_url, self_)
                db.session.add(track)
                db.session.commit()
                # Significa que retorno con exito
                resp.status_code = 201
                return resp
        else:
            # Significa que no existe el album
            resp = jsonify({})
            resp.status_code = 422
            return resp
    
    elif request.method == 'GET':
        # Se crea la query
        get = db.session.query(Cancion).filter(Cancion.album_id == album_id).all()
        if get:
            resultado = []
            for row in get:
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
                'error': 'Album no encontrado.'
            })
            resp.status_code = 404
            return resp
    
    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp


@albumnes.route('/albums/<string:album_id>', methods=['GET', 'DELETE'])
def albums_artistId(album_id):
    if request.method == 'GET':
        # Se crea la query
        row = db.session.query(Album).filter(Album.id == album_id).all()
        if row:
            resp = jsonify({
                'id': row[0].id,
                'artist_id': row[0].artist_id,
                'name': row[0].name,
                'genre': row[0].genre,
                'artist': row[0].artist,
                'tracks': row[0].tracks,
                'self': row[0].self_
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
        # Se crea la query
        result = db.session.query(Album).filter(Album.id == album_id).all()
        if result:
            db.session.delete(result[0])
            db.session.commit()
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
    
    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp
    
"""
@albumnes.route('/albums/<string:album_id>/tracks/play')
def albums_albumId_tracks_play(album_id):
    if request.method == 'POST':
        pass
        #TODO
    else:
        resp = jsonify({
                'error': 'Metodo HTTP inexistente.'
            })
        resp.status_code = 405
        return resp
"""