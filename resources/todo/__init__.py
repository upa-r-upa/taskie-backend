from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from models import db, Todo

todo_namespace = Namespace("todo", description="Todo API")

todo_create_model = todo_namespace.model(
    "TodoCreate",
    {"title": fields.String(required=True), "content": fields.String(required=False)},
)


@todo_namespace.route("/<int:id>")
class TodoResource(Resource):
    @jwt_required()
    def get(self, id):
        todo = Todo.query.get(id)

        if not todo:
            return {"msg": "Todo not found"}, 404

        return {
            "msg": "Todo found",
            "todo": {"id": todo.id, "title": todo.title, "content": todo.content},
        }, 200


@todo_namespace.route("")
class TodoList(Resource):
    @todo_namespace.expect(todo_create_model, validate=True)
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            title = data.get("title")
            content = data.get("content")

            if not title:
                return {"msg": "Title is required"}, 400

            todo = Todo(title=title, content=content, user_id=get_jwt_identity())

            db.session.add(todo)
            db.session.commit()

            return {
                "msg": "Todo created",
                "todo": {"id": todo.id, "title": todo.title, "content": todo.content},
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": "An error occurred"}, 500
