DROP TABLE IF EXISTS Artista;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Cancion;

CREATE TABLE Artista (
    id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    albums TEXT,
    tracks TEXT,
    self TEXT
);

CREATE TABLE Album (
    id TEXT PRIMARY KEY,
    artist_id TEXT,
    name TEXT,
    genre TEXT,
    artist TEXT,
    tracks TEXT,
    self TEXT,
    FOREIGN KEY (artist_id) REFERENCES Artista (id)
);

CREATE TABLE Cancion (
    id TEXT PRIMARY KEY,
    album_id TEXT,
    name TEXT,
    duration FLOAT,
    times_played INTEGER,
    artist TEXT,
    album TEXT,
    self TEXT,
    FOREIGN KEY (album_id) REFERENCES Album (id)
);