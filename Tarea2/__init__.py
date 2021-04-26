from flask import Flask 

from .commands import create_tables
from .extensions import db
from .routes.artists import artistas
from .routes.albums import albumnes
from .routes.tracks import canciones


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.cli.add_command(create_tables)
    app.register_blueprint(artistas)
    app.register_blueprint(albumnes)
    app.register_blueprint(canciones)


    return app