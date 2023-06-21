from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

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
            return {"msg": "Username is required"}, 400

        if not password:
            return {"msg": "Password is required"}, 400

        if not password_check:
            return {"msg": "Password check is required"}, 400

        if not email:
            return {"msg": "Email is required"}, 400

        if password != password_check:
            return {"msg": "Password and password check must be same"}, 400

        if User.query.filter_by(username=username).first():
            return {"msg": "Username already exists"}, 400

        if User.query.filter_by(email=email).first():
            return {"msg": "Email already exists"}, 400

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
            return {"msg": "An error occurred"}, 500

        return {"msg": "User signup successful"}, 201


login_model = user_namespace.model(
    "Login",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)


@user_namespace.route("/auth/login")
class Login(Resource):
    @user_namespace.expect(login_model, validate=True)
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username:
            return {"msg": "Username is required"}, 400

        if not password:
            return {"msg": "Password is required"}, 400

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"msg": "Username or password is wrong"}, 400

        if not check_password_hash(user.password, password):
            return {"msg": "Username or password is wrong"}, 400

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200


@user_namespace.route("/auth/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)

        return {"access_token": access_token}, 200
