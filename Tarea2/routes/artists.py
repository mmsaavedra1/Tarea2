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


def codificar_id(name):
    encoded = b64encode(name.encode()).decode('utf-8')
    return encoded[:22]


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

        # Intenta crear el objeto
        try:
            artista = Artista(id_, name, age, albums_url, tracks_url, self_)
            db.session.add(artista)
            db.session.commit()

            # Significa que retorno con exito
            resp.status_code = 201
            return resp

        except:
                # Significa que ya existe en BD
            resp.status_code = 409
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
        
        if len(query) != 0:
            try:
                # params
                id_ = b64encode(name.encode()).decode('utf-8')[:22]
                artist_url = f'{os.environ.get("HEROKU_URL")}artists/{artist_id}'
                tracks_url = f'{os.environ.get("HEROKU_URL")}albums/{id_}/tracks'
                self_ = f'{os.environ.get("HEROKU_URL")}albums/{id_}'
                # response
                resp = jsonify({
                    'id': id_,
                    'artist_id': query[0].id,
                    'name': name,
                    'genre': genre,
                    'artist': artist_url,
                    'tracks': tracks_url,
                    'self': self_
                })

                album = Album(id_, query[0].id, name, genre, artist_url, tracks_url, self_)
                db.session.add(album)
                db.session.commit()

                # Significa que retorno con exito
                resp.status_code = 201
                return resp

            except:
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
        # Se crea la query
        get = db.session.query(Album).filter(artist_id == artist_id)
        if get:
            resultado = []
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
        get = db.session.query(Cancion).filter(Cancion.artist == f"{os.environ.get('HEROKU_URL')}artists/{artist_id}")
        if get:
            resultado = []
            for row in get.all():
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
        row = db.session.query(Artista).filter(Artista.id == artist_id)
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
        

@artistas.route('/artists/<string:artist_id>/albums/play')
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
