import os
from datetime import timedelta
import dotenv

dotenv.load_dotenv()

DATABASE_URI = os.environ.get("TSK_DB_URL")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
