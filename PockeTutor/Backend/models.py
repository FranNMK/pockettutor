from datetime import datetime
from .extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(190), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(120))
    verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.Enum('user','admin'), default='user')
    subscription = db.Column(db.Enum('free','premium'), default='free')
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=db.func.now()
    )

class FlashcardSet(db.Model):
    __tablename__ = "flashcard_sets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200))
    source_type = db.Column(db.Enum('paste','pdf','docx'), nullable=False)
    summary = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=db.func.now()
    )

class Flashcard(db.Model):
    __tablename__ = "flashcards"
    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey("flashcard_sets.id"), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    kind = db.Column(db.Enum('free','premium','ai_generated'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=db.func.now()
    )

class CourseSection(db.Model):
    __tablename__ = "course_sections"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    section_title = db.Column(db.String(200), nullable=False)
    order_index = db.Column(db.Integer, default=0)

class CourseLesson(db.Model):
    __tablename__ = "course_lessons"
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey("course_sections.id"), nullable=False)
    lesson_title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    youtube_url = db.Column(db.String(255))
    reference_links = db.Column(db.Text)  # JSON string
    order_index = db.Column(db.Integer, default=0)

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    progress_percent = db.Column(db.Integer, default=0)
    started_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=db.func.now()
    )
    completed_at = db.Column(db.DateTime, nullable=True)

class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    kind = db.Column(db.Enum('section','final'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer)
    passed = db.Column(db.Boolean, default=False)
    taken_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=db.func.now()
    )
