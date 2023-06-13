from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from . import config

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        from .models import db

        db.init_app(app)

    migrate.init_app(app, db)

    return app
