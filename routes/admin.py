from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from extensions import db
from models import Company, Job, StudentProfile, Application, PlacementNotice, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _require_admin():
    if not current_user.is_admin():
        abort(403)


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    _require_admin()
    stats = {
        "students": StudentProfile.query.count(),
        "companies": Company.query.count(),
        "jobs": Job.query.filter_by(is_active=True).count(),
        "applications": Application.query.count(),
        "selected": Application.query.filter_by(status="Selected").count(),
    }
    recent_applications = Application.query.order_by(Application.applied_at.desc()).limit(10).all()
    return render_template("admin/dashboard.html", stats=stats, recent_applications=recent_applications)


# ---------- Companies ----------

@admin_bp.route("/companies", methods=["GET", "POST"])
@login_required
def companies():
    _require_admin()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Company name is required.", "warning")
        else:
            company = Company(
                name=name,
                description=request.form.get("description", ""),
                website=request.form.get("website", ""),
            )
            db.session.add(company)
            db.session.commit()
            flash("Company added.", "success")
        return redirect(url_for("admin.companies"))

    all_companies = Company.query.order_by(Company.name).all()
    return render_template("admin/companies.html", companies=all_companies)


@admin_bp.route("/companies/<int:company_id>/delete", methods=["POST"])
@login_required
def delete_company(company_id):
    _require_admin()
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash("Company removed.", "info")
    return redirect(url_for("admin.companies"))


# ---------- Jobs ----------

@admin_bp.route("/jobs", methods=["GET", "POST"])
@login_required
def jobs():
    _require_admin()
    if request.method == "POST":
        drive_date_str = request.form.get("drive_date", "")
        drive_date = None
        if drive_date_str:
            try:
                drive_date = datetime.strptime(drive_date_str, "%Y-%m-%d").date()
            except ValueError:
                drive_date = None

        job = Job(
            company_id=request.form.get("company_id"),
            title=request.form.get("title", "").strip(),
            description=request.form.get("description", ""),
            required_skills=request.form.get("required_skills", ""),
            min_cgpa=float(request.form.get("min_cgpa") or 0),
            package_lpa=float(request.form.get("package_lpa") or 0),
            location=request.form.get("location", ""),
            drive_date=drive_date,
            is_active=True,
        )
        db.session.add(job)
        db.session.commit()
        flash("Job posted.", "success")
        return redirect(url_for("admin.jobs"))

    all_jobs = Job.query.order_by(Job.id.desc()).all()
    all_companies = Company.query.order_by(Company.name).all()
    return render_template("admin/jobs.html", jobs=all_jobs, companies=all_companies)


@admin_bp.route("/jobs/<int:job_id>/toggle", methods=["POST"])
@login_required
def toggle_job(job_id):
    _require_admin()
    job = Job.query.get_or_404(job_id)
    job.is_active = not job.is_active
    db.session.commit()
    flash(f"Job {'activated' if job.is_active else 'deactivated'}.", "info")
    return redirect(url_for("admin.jobs"))


@admin_bp.route("/jobs/<int:job_id>/delete", methods=["POST"])
@login_required
def delete_job(job_id):
    _require_admin()
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash("Job removed.", "info")
    return redirect(url_for("admin.jobs"))


@admin_bp.route("/jobs/<int:job_id>/applicants")
@login_required
def job_applicants(job_id):
    _require_admin()
    job = Job.query.get_or_404(job_id)
    apps = Application.query.filter_by(job_id=job.id).order_by(Application.match_score.desc()).all()
    return render_template("admin/job_applicants.html", job=job, applications=apps)


@admin_bp.route("/applications/<int:app_id>/status", methods=["POST"])
@login_required
def update_application_status(app_id):
    _require_admin()
    application = Application.query.get_or_404(app_id)
    new_status = request.form.get("status")
    if new_status in ("Applied", "Shortlisted", "Rejected", "Selected"):
        application.status = new_status
        db.session.commit()
        flash("Application status updated.", "success")
    return redirect(request.referrer or url_for("admin.dashboard"))


# ---------- Students ----------

@admin_bp.route("/students")
@login_required
def students():
    _require_admin()
    all_students = StudentProfile.query.all()
    return render_template("admin/students.html", students=all_students)


@admin_bp.route("/students/<int:profile_id>")
@login_required
def student_detail(profile_id):
    _require_admin()
    profile = StudentProfile.query.get_or_404(profile_id)
    apps = Application.query.filter_by(student_id=profile.id).all()
    return render_template("admin/student_detail.html", profile=profile, applications=apps)


# ---------- Notices ----------

@admin_bp.route("/notices", methods=["GET", "POST"])
@login_required
def notices():
    _require_admin()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "")
        if title:
            notice = PlacementNotice(title=title, content=content)
            db.session.add(notice)
            db.session.commit()
            flash("Notice published.", "success")
        return redirect(url_for("admin.notices"))

    all_notices = PlacementNotice.query.order_by(PlacementNotice.created_at.desc()).all()
    return render_template("admin/notices.html", notices=all_notices)


@admin_bp.route("/notices/<int:notice_id>/delete", methods=["POST"])
@login_required
def delete_notice(notice_id):
    _require_admin()
    notice = PlacementNotice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    flash("Notice deleted.", "info")
    return redirect(url_for("admin.notices"))
