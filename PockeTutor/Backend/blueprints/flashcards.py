# backend/blueprints/flashcards.py
import os, tempfile
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import FlashcardSet, Flashcard
from ..utils.flashcards import generate_flashcards
from ..utils.pdf_tools import extract_text_from_file  # ✅ import our helper
# backend/blueprints/flashcards.py (add)
from flask import send_file
from ..utils.export import export_flashcards_pdf
import tempfile

@flash_bp.get("/<int:set_id>/export/pdf")
def export_pdf(set_id):
    fc_set = FlashcardSet.query.get_or_404(set_id)
    cards = Flashcard.query.filter_by(set_id=set_id).all()
    flashcards = [{"question": c.question, "answer": c.answer} for c in cards]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.close()
    export_flashcards_pdf(fc_set.title or "Flashcards", flashcards, tmp.name)
    return send_file(tmp.name, as_attachment=True, download_name=f"{fc_set.title or 'flashcards'}.pdf")

flash_bp = Blueprint("flashcards", __name__, url_prefix="/api/flashcards")

@flash_bp.route("/from-file", methods=["POST"])
def from_file():
    """
    multipart/form-data with fields:
    - user_id (int)
    - title (optional)
    - file (pdf or docx)
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    user_id = request.form.get("user_id")
    title = request.form.get("title", "Imported flashcards")
    f = request.files["file"]

    # Save uploaded file to temporary dir
    tmpdir = tempfile.mkdtemp()
    filename = f.filename
    path = os.path.join(tmpdir, filename)
    f.save(path)

    try:
        # ✅ clean extraction using our helper
        extracted = extract_text_from_file(path)

        # call AI hook to generate flashcards
        qa_list = generate_flashcards(extracted, n=10)

        # optional summary (could be empty if AI doesn’t return it)
        summary = ""
        if isinstance(qa_list, dict):
            summary = qa_list.get("summary", "")
            qa = qa_list.get("qa", [])
        else:
            qa = qa_list

        # store in DB
        fc_set = FlashcardSet(
            user_id=int(user_id),
            title=title,
            source_type="pdf" if filename.lower().endswith(".pdf") else "docx",
            summary=summary,
        )
        db.session.add(fc_set)
        db.session.flush()  # so fc_set.id is available

        for item in qa:
            q = item.get("q") or item.get("question") or ""
            a = item.get("a") or item.get("answer") or ""
            db.session.add(Flashcard(set_id=fc_set.id, question=q, answer=a))

        db.session.commit()

    finally:
        try:
            os.remove(path)
        except:
            pass

    return jsonify({"set_id": fc_set.id, "summary": summary, "count": len(qa)}), 201
