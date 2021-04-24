import os

from flask import Flask
from .extensions import db
from .commands import create_tables


def create_app(test_config=None):
    # Crea y configura la App
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Configura la base de datos
    db.init_app(app)
    app.cli.add_command(create_tables)

    # Create routes
    from . import artists
    app.register_blueprint(artists.bp)
    #app.add_url_rule('/', endpoint='index')

    from . import albums
    app.register_blueprint(albums.bp)
    #app.add_url_rule('/', endpoint='index')

    from . import tracks
    app.register_blueprint(tracks.bp)
    #app.add_url_rule('/', endpoint='index')

    return app