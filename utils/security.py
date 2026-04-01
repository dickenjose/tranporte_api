import bcrypt
from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = "secret123"

def verificar_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


def crear_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
