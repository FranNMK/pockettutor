from flask import Flask
from .config import Config
from .extensions import db, bcrypt, mail, cors
from .blueprints.auth import auth_bp
from .blueprints.flashcards import flash_bp
from .blueprints.courses import courses_bp
from .blueprints.progress import progress_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    cors.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(flash_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(progress_bp)

    @app.get("/api/health")
    def health():
        return {"ok": True}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
