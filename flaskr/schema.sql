DROP TABLE IF EXISTS Artista;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Cancion;

CREATE TABLE Artista (
    id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    albums TEXT,
    tracks TEXT,
    selg TEXT
);

CREATE TABLE Album (
    id TEXT PRIMARY KEY,
    name TEXT,
    genre TEXT,
    artist TEXT,
    tracks TEXT,
    self TEXT,
    FOREIGN KEY (id) REFERENCES Artista (id)
);

CREATE TABLE Cancion (
    id TEXT PRIMARY KEY,
    name TEXT,
    duration FLOAT,
    times_played INTEGER,
    artist TEXT,
    album TEXT,
    self TEXT,
    FOREIGN KEY (id) REFERENCES Album (id)
);