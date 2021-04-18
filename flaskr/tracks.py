from flask import (Flask, g, request, Blueprint)
from werkzeug.exceptions import abort
from flaskr.db import get_db

bp = Blueprint('tracks', __name__, )

@bp.route('/')
def index():
    db = get_db()


