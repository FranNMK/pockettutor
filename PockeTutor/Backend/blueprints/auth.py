from flask import Blueprint, request, jsonify, current_app
from ..extensions import db, bcrypt, mail
from ..models import User
from ..utils.tokens import generate_token, verify_token
from flask_mail import Message
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
@auth_bp.post("/login")
# backend/blueprints/auth.py (login)
from flask_jwt_extended import create_access_token

@auth_bp.post("/login")
def login():
    data = request.json
    email = data.get("email"); password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error":"Invalid credentials"}), 401
    if not user.verified:
        return jsonify({"error":"Email not verified"}), 403
    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify({"access_token": access_token, "user": {"id":user.id,"name":user.name,"email":user.email}}), 200

    data = request.json
    email = data.get("email"); password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error":"Invalid credentials"}), 401
    if not user.verified:
        return jsonify({"error":"Email not verified"}), 403
    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify({"access_token": access_token, "user": {"id":user.id,"name":user.name,"email":user.email}}), 200
Protect endpoints:
# backend/blueprints/auth.py (login)
from flask_jwt_extended import create_access_token

@auth_bp.post("/login")
def login():
    data = request.json
    email = data.get("email"); password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error":"Invalid credentials"}), 401
    if not user.verified:
        return jsonify({"error":"Email not verified"}), 403
    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify({"access_token": access_token, "user": {"id":user.id,"name":user.name,"email":user.email}}), 200


python
Copy code
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

@courses_bp.post("/generate")
@jwt_required()
def generate():
    user_id = get_jwt_identity()
    # enforce daily limit logic here...
@auth_bp.post("/signup")
def signup():
    data = request.json
    name = data.get("name"); email = data.get("email"); password = data.get("password"); country = data.get("country")
    if not all([name, email, password]):
        return jsonify({"error":"Missing fields"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error":"Email already registered"}), 409
    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(name=name, email=email, password_hash=pw_hash, country=country, verified=False)
    db.session.add(user); db.session.commit()
    token = generate_token(email)
    verify_link = f"{request.host_url}api/auth/verify/{token}"
    msg = Message(subject="Verify your PocketTutor account", recipients=[email], body=f"Verify here: {verify_link}")
    mail.send(msg)
    return jsonify({"message":"Signup successful. Check your email to verify.", "verify_link_debug": verify_link}), 201

@auth_bp.get("/verify/<token>")
def verify_email(token):
    try:
        email = verify_token(token)
    except Exception:
        return jsonify({"error":"Invalid or expired token"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error":"User not found"}), 404
    if user.verified:
        return jsonify({"message":"Already verified"}), 200
    user.verified = True
    db.session.commit()
    return jsonify({"message":"Email verified. You can now log in."}), 200

@auth_bp.post("/login")
def login():
    data = request.json
    email = data.get("email"); password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error":"Invalid credentials"}), 401
    if not user.verified:
        return jsonify({"error":"Email not verified"}), 403
    # For simplicity, return a dumb session token (in prod use JWT)
    return jsonify({"message":"Login ok", "user":{"id":user.id,"name":user.name,"email":user.email}}), 200
