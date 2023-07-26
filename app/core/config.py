import os
from datetime import timedelta
import dotenv

dotenv.load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get("TSK_SQLALCHEMY_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "비밀키")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
