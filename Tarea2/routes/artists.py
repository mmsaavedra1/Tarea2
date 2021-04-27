from flask import (Flask, g, request, Blueprint, jsonify)
from werkzeug.exceptions import abort
from base64 import b64encode
import sqlite3
import json
import os

from Tarea2.extensions import db
from sqlalchemy import text
from Tarea2.models import *

artistas = Blueprint('artistas', __name__)



@artistas.route('/artists', methods=['GET', 'POST'])
def artists():
    if request.method ==  'POST':
        # Comprueba que el body está bien hecho
        valores = request.json
        if ("name" not in valores) or ("age" not in valores):
        #if ((name == None) or (age == None)):
            resp = jsonify({
                    'error': f"Input invalido en json",
                })
            resp.status_code = 400

            return resp
        else:
            name = valores["name"]
            age = valores["age"]

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
        
        # Comprueba si existe o no el artista
        get = db.session.query(Artista).filter(Artista.id == id_).all()
        if get:           
            resp.status_code = 409
            return resp

        else:
            artista = Artista(id_, name, age, albums_url, tracks_url, self_)
            db.session.add(artista)
            db.session.commit()

            # Significa que retorno con exito
            resp.status_code = 201
            return resp

    elif request.method == 'GET':

        # Se guardan los resultados
        resultado = []
        
        # Se crea la consulta
        get = db.session.query(Artista)

        for row in get.all():
            resultado.append({
                'id': row.id,
                'name': row.name,
                'age': row.age,
                'albums': row.albums,
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


@artistas.route('/artists/<string:artist_id>/albums', methods=['POST', 'GET'])
def artist_artistId_albums(artist_id):
    if request.method == 'POST':
        # Comprueba que el body está bien hecho
        valores = request.json
        if ("name" not in valores) or ("genre" not in valores):
            resp = jsonify({
                    'error': f"Input invalido en json",
                })
            resp.status_code = 400

            return resp
        else:
            name = valores["name"]
            genre = valores["genre"]
    
        # Comrprobar que el artista existe para crear un album
        query = db.session.query(Artista).filter(Artista.id == artist_id).all()
        
        if query:
            #Body Request
            id_ = b64encode(f"{name}:{query[0].id}".encode()).decode('utf-8')[:22]
            artist_url = f'{os.environ.get("HEROKU_URL")}artists/{artist_id}'
            tracks_url = f'{os.environ.get("HEROKU_URL")}albums/{id_}/tracks'
            self_ = f'{os.environ.get("HEROKU_URL")}albums/{id_}'

            query2 = db.session.query(Album).filter(Album.id == id_).all()
            # response
            resp = jsonify({
                'name': name,
                'genre': genre,
                'artist': artist_url,
                'tracks': tracks_url,
                'self': self_
            })
            if len(query2) != 0:
                # Significa que ya existe en BD el album
                resp.status_code = 409
                return resp
            else:
                album = Album(id_, artist_id, name, genre, artist_url, tracks_url, self_)
                db.session.add(album)
                db.session.commit()
                # Significa que retorno con exito
                resp.status_code = 201
                return resp
        else:
            # Significa que no existe el artista previo
            resp = jsonify({})
            resp.status_code = 422
            return resp

    elif request.method == 'GET':
        # Se crea la query
        get = db.session.query(Album).filter(Album.artist_id == artist_id).all()
        if get:
            resultado = []
            for row in get:
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


@artistas.route('/artists/<string:artist_id>/tracks', methods=['GET'])
def artist_artistId_tracks(artist_id):
    if request.method == 'GET':
        # Se crea la query
        get = db.session.query(Cancion).filter(Cancion.artist == f"{os.environ.get('HEROKU_URL')}artists/{artist_id}").all()
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

# TODO: No esta eliminando en casacada
@artistas.route('/artists/<string:artist_id>', methods=['GET', 'DELETE'])
def artist_artistId(artist_id):
    if request.method == 'GET':
        # Se crea la query
        row = db.session.query(Artista).filter(Artista.id == artist_id).all()
        if row:
            resp = jsonify({
                'id': row[0].id,
                'name': row[0].name,
                'age': row[0].age,
                'albums': row[0].albums,
                'tracks': row[0].tracks,
                'self': row[0].self_
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
        # Se crea la query
        row = db.session.query(Artista).filter(Artista.id == artist_id).all()
        if row:
            db.session.delete(row[0])   
            db.session.commit()
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
        
# 200 (OK), 404 (Not found)
@artistas.route('/artists/<string:artist_id>/albums/play', methods=['PUT'])
def artist_artistId_albums_play(artist_id):
    if request.method == 'PUT':
        resp = jsonify({})
        artist = db.session.query(Artista).filter(Artista.id == artist_id).all()
        # Si existe el artista se prosigue
        if artist:
            albums = db.session.query(Album).filter(Album.artist_id == artist_id).all()
            if albums:
                for album in albums:
                    album_id = album.id
                    tracks = db.session.query(Cancion).filter(Cancion.album_id == album_id).all()
                    if tracks:
                        for track in tracks:
                            value = track.times_played + 1
                            track.times_played = value
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
