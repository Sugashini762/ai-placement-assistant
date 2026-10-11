# AI Placement Assistant

A Flask-based web application for a college's placement cell, combining:

- **Resume Analysis** — upload a PDF/DOCX/TXT resume and get an instant 0-100 score with feedback, based on skill keyword matching, section completeness, length, and quantified achievements.
- **Smart Job Matching** — ranks active job openings for each student by skill overlap and CGPA eligibility.
- **Mock Interview Practice** — role-based interview questions (Software Engineer, Data Analyst, HR/Behavioral) scored via keyword-coverage analysis of free-text answers.
- **Placement Chatbot** — a rule-based FAQ assistant answering questions about eligibility, process, dates, and more, enriched with live data from the database.
- **Admin / Placement Cell Dashboard** — manage companies, jobs, students, applications, and notices.

Everything runs **fully offline** — no external/paid AI API keys are required, which makes it easy to run and demo for an academic project.

## 1. Setup

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed the database (creates tables + demo admin/companies/jobs)
python seed.py

# 4. Run the app
python app.py
```

The app will be available at **http://127.0.0.1:5000**

## 2. Demo Login

- **Admin:** `admin@college.edu` / `admin123`
- **Student:** register a new account from the homepage.

## 3. Project Structure

```
ai_placement_assistant/
├── app.py                 # Flask app factory & entrypoint
├── config.py               # App configuration
├── extensions.py            # Shared db / login_manager instances
├── models.py                # SQLAlchemy models
├── seed.py                  # Demo data seeding script
├── requirements.txt
├── routes/
│   ├── auth.py               # Register / login / logout
│   ├── main.py                # Landing page + chatbot API
│   ├── student.py             # Student dashboard, resume, jobs, interview
│   └── admin.py               # Placement cell dashboard
├── utils/
│   ├── skill_bank.py           # Skill list + interview question bank (data)
│   ├── resume_parser.py         # Resume text extraction & scoring logic
│   ├── matcher.py                # Job <-> student matching algorithm
│   ├── interview_engine.py        # Interview question selection & scoring
│   └── chatbot_engine.py           # Rule-based chatbot intent matching
├── templates/                # Jinja2 HTML templates (Bootstrap 5)
└── static/css/style.css       # Custom theme
```

## 4. How the "AI" works (no paid API needed)

| Feature | Technique |
|---|---|
| Resume scoring | Keyword matching against a curated skill bank + heuristics (sections, length, contact info, quantified achievements) |
| Job matching | Skill-set overlap (Jaccard-style score) + CGPA eligibility check |
| Mock interview | Keyword-coverage scoring of free-text answers against ideal-answer keyword sets |
| Chatbot | Rule-based intent matching (keyword + fuzzy matching) enriched with live DB data |

This design is intentionally transparent and explainable — useful for a viva/demo where you may be asked "how does the AI actually work?"

## 5. Customization ideas (see chat for the full roadmap)

- Swap the resume/interview keyword-matching logic for a real ML model (e.g., TF-IDF + cosine similarity, or spaCy NER) for extra marks.
- Add email notifications when application status changes.
- Add a company-side login to post jobs directly.
- Deploy to Render / PythonAnywhere / Railway for a live demo link.
