from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Course, CourseSection, CourseLesson, Enrollment
from datetime import datetime, timedelta
from ..models import User, Enrollment, Course
courses_bp = Blueprint("courses", __name__, url_prefix="/api/courses")
@courses_bp.post("/generate")
@jwt_required()
def generate():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    # check premium
    if user.subscription == 'premium':
        allow = True
    else:
        # check last generation timestamp stored on user (add column last_course_generated)
        last = user.last_course_generated  # add to model if not present
        if last and last.date() == datetime.utcnow().date():
            # still same day
            # require >=50% progress on existing generated course or payment
            enr = Enrollment.query.filter_by(user_id=uid, course_id=user.current_generated_course_id).first()
            if not enr or enr.progress_percent < 50:
                return jsonify({"error":"Daily limit reached. Complete 50% or upgrade/pay."}), 403
        allow = True
    # generate course...
    # after successful generation update user.last_course_generated = datetime.utcnow() and user.current_generated_course_id = new_course.id
@courses_bp.get("/library")
def library():
    items = Course.query.with_entities(Course.id, Course.title, Course.description, Course.kind).all()
    return jsonify([{"id":i.id,"title":i.title,"description":i.description,"kind":i.kind} for i in items]), 200

@courses_bp.post("/generate")
def generate():
    data = request.json
    user_id = data.get("user_id")
    topic = data.get("topic","")
    if not topic:
        return jsonify({"error":"Missing topic"}), 400
    # TODO: call AI to generate a structured course
    course = Course(title=f"{topic} – Starter Course", description="AI-generated outline", kind="ai_generated", created_by=user_id)
    db.session.add(course); db.session.flush()

    sec = CourseSection(course_id=course.id, section_title="Introduction", order_index=1)
    db.session.add(sec); db.session.flush()
    lesson = CourseLesson(section_id=sec.id, lesson_title=f"What is {topic}?", content="Placeholder content", youtube_url="", reference_links="[]", order_index=1)
    db.session.add(lesson)
    db.session.commit()

    return jsonify({"course_id": course.id, "title": course.title}), 201

@courses_bp.post("/enroll")
def enroll():
    data = request.json
    user_id = data.get("user_id"); course_id = data.get("course_id")
    if not all([user_id, course_id]):
        return jsonify({"error":"Missing fields"}), 400
    if Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first():
        return jsonify({"message":"Already enrolled"}), 200
    db.session.add(Enrollment(user_id=user_id, course_id=course_id, progress_percent=0))
    db.session.commit()
    return jsonify({"message":"Enrolled"}), 201
# Backend/models/course.py
class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ link to User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="courses")

    progress = db.Column(db.Integer, default=0)  # % completed
# Backend/routes/courses.py
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Course, User

@courses_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate_course():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # check last course generated
    last_course = Course.query.filter_by(user_id=user.id).order_by(Course.created_at.desc()).first()

    if last_course:
        # enforce 1 course/day unless 50% complete
        too_soon = last_course.created_at > datetime.utcnow() - timedelta(days=1)
        not_done = last_course.progress < 50
        if too_soon and not_done:
            return jsonify({"error": "Finish 50% of your current course or wait until tomorrow."}), 403

    # else → generate new course here
    new_course = Course(title="AI Generated Course", user_id=user.id)
    db.session.add(new_course)
    db.session.commit()

    return jsonify({"message": "Course generated!", "course_id": new_course.id})
