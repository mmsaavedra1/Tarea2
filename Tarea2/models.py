from werkzeug.security import generate_password_hash

from .extensions import db 

class Artista(db.Model):
    id = db.Column("id", db.Text, primary_key=True)
    name = db.Column("name", db.Text)
    age = db.Column("age", db.Integer)
    albums = db.Column("albums", db.Text)
    tracks = db.Column("tracks", db.Text)
    self_ = db.Column("self", db.Text)

    def __init__(self, id, name, age, albums, tracks, self_):
        self.id = id
        self.name = name
        self.age = age
        self.albums = albums
        self.tracks = tracks
        self.self_ = self_


class Album(db.Model):
    id = db.Column("id", db.Text, primary_key=True)
    artist_id = db.Column("artist_id", db.Text, db.ForeignKey('artista.id', ondelete='CASCADE'), nullable=False,)
    name = db.Column("name", db.Text)
    genre = db.Column("genre", db.Integer)
    artist = db.Column("artist", db.Text)
    tracks = db.Column("tracks", db.Text)
    self_ = db.Column("self", db.Text)

    def __init__(self, id, artist_id, name, genre, artist, tracks, self_):
        self.id = id
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.artist = artist
        self.tracks = tracks
        self.self_ = self_


class Cancion(db.Model):
    id = db.Column("id", db.Text, primary_key=True)
    album_id = db.Column("album_id", db.Text, db.ForeignKey('album.id', ondelete='CASCADE'), nullable=False,)
    name = db.Column("name", db.Text)
    duration = db.Column("duration", db.Float)
    times_played = db.Column("times_played", db.Integer)
    artist = db.Column("artist", db.Text)
    album = db.Column("album", db.Text)
    self_ = db.Column("self", db.Text)

    def __init__(self, id, album_id, name, duration, times_played, artist, album, self_):
        self.id = id
        self.album_id = album_id
        self.name = name
        self.duration = duration
        self.times_played = times_played
        self.artist = artist
        self.album = album
        self.self_ = self_
        
    