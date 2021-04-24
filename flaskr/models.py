from .extensions import db

class Artista(db.Model):
    id = db.Column("id", db.Text, primary_key=True)
    name = db.Column("name", db.Text)
    age = db.Column("age", db.Integer)
    albums = db.Column("albums", db.Text)
    tracks = db.Column("tracks", db.Text)
    self_ = db.Column("self", db.Text)


class Album(db.Model):
    id = db.Column("id", db.Text, primary_key=True)
    artist_id = db.Column("artist_id", db.Text, ForeignKey('artista.id', ondelete='CASCADE'), nullable=False,)
    name = db.Column("name", db.Text)
    genre = db.Column("genre", db.Integer)
    artist = db.Column("artist", db.Text)
    tracks = db.Column("tracks", db.Text)
    self_ = db.Column("self", db.Text)


class Cancion(db.Model):
    id = db.Column("id", db.Text, primary_key=True)
    album_id = db.Column("album_id", db.Text, ForeignKey('album.id', ondelete='CASCADE'), nullable=False,)
    name = db.Column("name", db.Text)
    duration = db.Column("duration", db.Float)
    times_played = db.Colummn("times_played", db.Integer)
    artist = db.Column("artist", db.Text)
    album = db.Column("album", db.Text)
    self_ = db.Column("self", db.Text)
    