from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Enrollment

progress_bp = Blueprint("progress", __name__, url_prefix="/api/progress")

@progress_bp.post("/update")
def update():
    data = request.json
    user_id = data.get("user_id"); course_id = data.get("course_id"); percent = int(data.get("percent",0))
    enr = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if not enr: return jsonify({"error":"Not enrolled"}), 404
    enr.progress_percent = max(0, min(100, percent))
    db.session.commit()
    return jsonify({"message":"Progress updated", "progress":enr.progress_percent}), 200
