import json
import os
import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user

from extensions import db
from models import Job, Application, InterviewSession, PlacementNotice
from utils.resume_parser import extract_text, score_resume, allowed_file
from utils.matcher import rank_jobs_for_student
from utils.interview_engine import get_roles, get_questions, evaluate_session

student_bp = Blueprint("student", __name__, url_prefix="/student")


def _require_student():
    if current_user.is_admin():
        abort(403)


@student_bp.route("/dashboard")
@login_required
def dashboard():
    _require_student()
    profile = current_user.profile
    notices = PlacementNotice.query.order_by(PlacementNotice.created_at.desc()).limit(5).all()
    applications = Application.query.filter_by(student_id=profile.id).all()
    recent_interviews = InterviewSession.query.filter_by(student_id=profile.id) \
        .order_by(InterviewSession.created_at.desc()).limit(3).all()

    top_jobs = rank_jobs_for_student(profile, Job.query.filter_by(is_active=True).all())[:5]

    return render_template(
        "student/dashboard.html",
        profile=profile,
        notices=notices,
        applications=applications,
        recent_interviews=recent_interviews,
        top_jobs=top_jobs,
    )


@student_bp.route("/resume", methods=["GET", "POST"])
@login_required
def resume():
    _require_student()
    profile = current_user.profile

    if request.method == "POST":
        file = request.files.get("resume_file")
        if not file or file.filename == "":
            flash("Please choose a resume file to upload.", "warning")
            return redirect(url_for("student.resume"))

        if not allowed_file(file.filename, current_app.config["ALLOWED_EXTENSIONS"]):
            flash("Unsupported file type. Please upload PDF, DOCX, or TXT.", "warning")
            return redirect(url_for("student.resume"))

        ext = file.filename.rsplit(".", 1)[1].lower()
        safe_name = f"{current_user.id}_{uuid.uuid4().hex[:8]}.{ext}"
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], safe_name)
        file.save(save_path)

        try:
            text = extract_text(save_path)
        except Exception as e:
            flash(f"Could not read the file: {e}", "danger")
            return redirect(url_for("student.resume"))

        if not text or not text.strip():
            flash("Could not extract any text from that file. Try a different format.", "warning")
            return redirect(url_for("student.resume"))

        score, feedback, skills = score_resume(text)

        profile.resume_filename = safe_name
        profile.resume_text = text
        profile.resume_score = score
        profile.resume_feedback = "\n".join(feedback)
        profile.extracted_skills = ", ".join(skills)
        db.session.commit()

        flash("Resume analyzed successfully!", "success")
        return redirect(url_for("student.resume"))

    return render_template("student/resume_upload.html", profile=profile)


@student_bp.route("/jobs")
@login_required
def jobs():
    _require_student()
    profile = current_user.profile
    all_jobs = Job.query.filter_by(is_active=True).all()
    ranked = rank_jobs_for_student(profile, all_jobs)

    applied_job_ids = {a.job_id for a in Application.query.filter_by(student_id=profile.id).all()}

    return render_template("student/jobs.html", ranked=ranked, applied_job_ids=applied_job_ids, profile=profile)


@student_bp.route("/jobs/<int:job_id>/apply", methods=["POST"])
@login_required
def apply_job(job_id):
    _require_student()
    profile = current_user.profile
    job = Job.query.get_or_404(job_id)

    existing = Application.query.filter_by(student_id=profile.id, job_id=job.id).first()
    if existing:
        flash("You have already applied to this job.", "info")
        return redirect(url_for("student.jobs"))

    from utils.matcher import compute_match_score
    score = compute_match_score(profile.skills_list(), job.skills_list())

    application = Application(student_id=profile.id, job_id=job.id, match_score=score)
    db.session.add(application)
    db.session.commit()

    flash(f"Applied to {job.title} at {job.company.name}!", "success")
    return redirect(url_for("student.jobs"))


@student_bp.route("/interview", methods=["GET"])
@login_required
def interview_setup():
    _require_student()
    roles = get_roles()
    return render_template("student/interview.html", roles=roles)


@student_bp.route("/interview/start/<role>", methods=["GET"])
@login_required
def interview_start(role):
    _require_student()
    questions = get_questions(role)
    if not questions:
        flash("Unknown interview role selected.", "warning")
        return redirect(url_for("student.interview_setup"))
    return render_template("student/interview_session.html", role=role, questions=questions)


@student_bp.route("/interview/submit/<role>", methods=["POST"])
@login_required
def interview_submit(role):
    _require_student()
    profile = current_user.profile
    questions = get_questions(role)
    if not questions:
        flash("Unknown interview role selected.", "warning")
        return redirect(url_for("student.interview_setup"))

    answers = [request.form.get(f"answer_{i}", "") for i in range(len(questions))]
    qa_results, overall_score = evaluate_session(questions, answers)

    session_obj = InterviewSession(
        student_id=profile.id,
        role=role,
        qa_json=json.dumps(qa_results),
        overall_score=overall_score,
    )
    db.session.add(session_obj)
    db.session.commit()

    return redirect(url_for("student.interview_result", session_id=session_obj.id))


@student_bp.route("/interview/result/<int:session_id>")
@login_required
def interview_result(session_id):
    _require_student()
    profile = current_user.profile
    session_obj = InterviewSession.query.get_or_404(session_id)
    if session_obj.student_id != profile.id:
        abort(403)
    qa_results = json.loads(session_obj.qa_json)
    return render_template("student/interview_result.html", session=session_obj, qa_results=qa_results)


@student_bp.route("/interview/history")
@login_required
def interview_history():
    _require_student()
    profile = current_user.profile
    sessions = InterviewSession.query.filter_by(student_id=profile.id) \
        .order_by(InterviewSession.created_at.desc()).all()
    return render_template("student/interview_history.html", sessions=sessions)


@student_bp.route("/applications")
@login_required
def applications():
    _require_student()
    profile = current_user.profile
    apps = Application.query.filter_by(student_id=profile.id).order_by(Application.applied_at.desc()).all()
    return render_template("student/applications.html", applications=apps)
