from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required

from models import Job, PlacementNotice, ChatLog
from extensions import db
from utils.chatbot_engine import get_response

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            from flask import redirect, url_for
            return redirect(url_for("admin.dashboard"))
        from flask import redirect, url_for
        return redirect(url_for("student.dashboard"))
    return render_template("index.html")


@main_bp.route("/chatbot", methods=["GET"])
@login_required
def chatbot_page():
    return render_template("student/chatbot.html")


@main_bp.route("/api/chatbot", methods=["POST"])
@login_required
def chatbot_api():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "Please type a question."})

    active_jobs_count = Job.query.filter_by(is_active=True).count()
    latest_notice_obj = PlacementNotice.query.order_by(PlacementNotice.created_at.desc()).first()
    latest_notice = latest_notice_obj.title if latest_notice_obj else None

    response = get_response(message, active_jobs_count=active_jobs_count, latest_notice=latest_notice)

    log = ChatLog(user_id=current_user.id, message=message, response=response)
    db.session.add(log)
    db.session.commit()

    return jsonify({"response": response})
