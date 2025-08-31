from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager
jwt = JWTManager()
# add jwt.init_app(app) in create_app


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
cors = CORS()
