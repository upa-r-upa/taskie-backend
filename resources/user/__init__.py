from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

user_namespace = Namespace("user", description="User API")

user_model = user_namespace.model(
    "User",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
        "password_check": fields.String(required=True),
        "email": fields.String(required=True),
        "grade": fields.Integer(required=False),
        "profile_image": fields.String(required=False),
        "nickname": fields.String(required=False),
    },
)


@user_namespace.route("/signup")
class Signup(Resource):
    @user_namespace.expect(user_model, validate=True)
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        password_check = data.get("password_check")
        email = data.get("email")
        grade = data.get("grade")
        profile_image = data.get("profile_image")
        nickname = data.get("nickname")

        if not username:
            return {"message": "Username is required"}, 400

        if not password:
            return {"message": "Password is required"}, 400

        if not password_check:
            return {"message": "Password check is required"}, 400

        if not email:
            return {"message": "Email is required"}, 400

        if password != password_check:
            return {"message": "Password and password check must be same"}, 400

        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 400

        password_hash = generate_password_hash(password)

        user = User(
            username=username,
            password=password_hash,
            email=email,
            grade=grade,
            profile_image=profile_image,
            nickname=nickname or username,
        )

        try:
            db.session.add(user)
            db.session.commit()

        except Exception as e:
            db.session.rollback()  # 롤백 처리
            return {"message": "An error occurred"}, 500

        return {"message": "User signup successful"}, 201
