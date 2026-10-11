"""
Run this once after installing dependencies to create the database tables
and populate demo data: an admin account, sample companies, jobs, and a
placement notice. This makes the project immediately demo-able.

Usage:
    python seed.py
"""

from datetime import date

from app import create_app
from extensions import db
from models import User, Company, Job, PlacementNotice

app = create_app()

with app.app_context():
    db.create_all()

    if User.query.filter_by(email="admin@college.edu").first() is None:
        admin = User(name="Placement Admin", email="admin@college.edu", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        print("Created admin user -> email: admin@college.edu | password: admin123")

    if Company.query.count() == 0:
        infosys = Company(name="Infosys", description="Global IT services and consulting.",
                           website="https://infosys.com")
        tcs = Company(name="TCS", description="IT services, consulting, and business solutions.",
                      website="https://tcs.com")
        startupx = Company(name="StartupX", description="Fast-growing product startup building SaaS tools.",
                            website="https://startupx.io")
        db.session.add_all([infosys, tcs, startupx])
        db.session.commit()

        jobs = [
            Job(company_id=infosys.id, title="Software Engineer Trainee",
                description="Work on enterprise applications using Java and Spring Boot.",
                required_skills="java, spring boot, sql, git, oop, data structures",
                min_cgpa=6.5, package_lpa=4.5, location="Bangalore",
                drive_date=date(2026, 8, 15)),
            Job(company_id=tcs.id, title="Data Analyst",
                description="Analyze business data and build dashboards for stakeholders.",
                required_skills="sql, python, excel, power bi, data analysis, statistics",
                min_cgpa=6.0, package_lpa=4.0, location="Chennai",
                drive_date=date(2026, 8, 20)),
            Job(company_id=startupx.id, title="Full Stack Developer Intern",
                description="Build features across our React frontend and Flask backend.",
                required_skills="python, flask, react, javascript, html, css, git, rest api",
                min_cgpa=7.0, package_lpa=6.0, location="Remote",
                drive_date=date(2026, 8, 25)),
            Job(company_id=startupx.id, title="Machine Learning Intern",
                description="Assist in building ML models for the recommendation engine.",
                required_skills="python, machine learning, pandas, numpy, scikit-learn, sql",
                min_cgpa=7.5, package_lpa=7.0, location="Remote",
                drive_date=date(2026, 9, 1)),
        ]
        db.session.add_all(jobs)
        print("Created sample companies and jobs.")

    if PlacementNotice.query.count() == 0:
        notice = PlacementNotice(
            title="Placement Season 2026-27 Registration Open",
            content="All final year students must complete their profile and upload their resume "
                    "before applying to any job. Registration closes soon, so apply early.",
        )
        db.session.add(notice)
        print("Created a sample placement notice.")

    db.session.commit()
    print("\nSeed complete. You can now run: python app.py")
