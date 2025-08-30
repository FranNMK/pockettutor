# backend/blueprints/admin.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..extensions import db
from ..models import Course, CourseSection, CourseLesson, User

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

def is_admin_from_identity():
    # Assume identity is user id, use DB to check role
    uid = get_jwt_identity()
    user = User.query.get(uid)
    return user and user.role == 'admin'

@admin_bp.post("/courses")
@jwt_required()
def create_course():
    if not is_admin_from_identity():
        return jsonify({"error":"Not authorized"}), 403
    data = request.json
    title = data.get("title"); desc = data.get("description","")
    course = Course(title=title, description=desc, kind=data.get("kind","free"))
    db.session.add(course); db.session.commit()
    return jsonify({"id": course.id, "title":course.title}), 201

@admin_bp.post("/courses/<int:course_id>/sections")
@jwt_required()
def add_section(course_id):
    if not is_admin_from_identity(): return jsonify({"error":"Not authorized"}), 403
    data = request.json
    sec = CourseSection(course_id=course_id, section_title=data.get("title"), order_index=data.get("order_index", 0))
    db.session.add(sec); db.session.commit()
    return jsonify({"id": sec.id, "title": sec.section_title}), 201

@admin_bp.post("/sections/<int:section_id>/lessons")
@jwt_required()
def add_lesson(section_id):
    if not is_admin_from_identity(): return jsonify({"error":"Not authorized"}), 403
    data = request.json
    lesson = CourseLesson(
        section_id=section_id,
        lesson_title=data.get("title"),
        content=data.get("content",""),
        youtube_url=data.get("youtube_url",""),
        reference_links=data.get("reference_links","[]"),
        order_index=data.get("order_index",0)
    )
    db.session.add(lesson); db.session.commit()
    return jsonify({"id":lesson.id}), 201
