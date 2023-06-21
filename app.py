from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager

migrate = Migrate()
api = Api()
jwt = JWTManager()


def register_namespaces():
    from resources.habit import habit_namespace
    from resources.routine import routine_namespace
    from resources.todo import todo_namespace
    from resources.user import user_namespace

    api.add_namespace(user_namespace)
    api.add_namespace(habit_namespace)
    api.add_namespace(routine_namespace)
    api.add_namespace(todo_namespace)


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    with app.app_context():
        from models import db

        db.init_app(app)

    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    register_namespaces()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
