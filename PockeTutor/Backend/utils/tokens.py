from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_token(email: str) -> str:
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt="email-verify")

def verify_token(token: str, max_age=3600*24):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.loads(token, salt="email-verify", max_age=max_age)
