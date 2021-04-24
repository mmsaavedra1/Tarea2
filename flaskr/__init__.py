import os

from flask import Flask

def create_app(test_config=None):
    # Crea y configura la App
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        DATABASE=os.environ.get("DATABASE_URL")
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

    # Create db into project
    from . import db
    db.init_app(app)

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