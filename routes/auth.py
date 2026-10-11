from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import User, StudentProfile

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.", "warning")
            return redirect(url_for("auth.register"))

        if password != confirm:
            flash("Passwords do not match.", "warning")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return redirect(url_for("auth.register"))

        user = User(name=name, email=email, role="student")
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # get user.id before commit

        profile = StudentProfile(user_id=user.id, branch=request.form.get("branch", ""),
                                  cgpa=float(request.form.get("cgpa") or 0))
        db.session.add(profile)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.name}!", "success")
            if user.is_admin():
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("student.dashboard"))

        flash("Invalid email or password.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
