import os
import base64
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET_KEY = base64.b64decode(os.getenv("JWT_SECRET_KEY"))
    JWT_ALGORITHM = "HS512"
