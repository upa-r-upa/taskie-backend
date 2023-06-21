import os
from datetime import timedelta

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
    os.path.join(BASE_DIR, "db", "taskie.db")
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "비밀키")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_TOKEN_LOCATION = ["cookies"]
JWT_ALGORITHM = "HS256"
