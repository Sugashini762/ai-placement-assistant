"""
Resume parsing and scoring module.

This is the core "AI" piece for resume analysis. It uses:
  - Text extraction from PDF / DOCX / TXT
  - Keyword matching against a curated skill bank
  - Section-completeness heuristics
  - A weighted scoring formula to produce a 0-100 resume score

No external paid API is required, so the project runs fully offline,
which keeps it easy to demo/run for an academic submission.
"""

import os
import re

from utils.skill_bank import SKILL_BANK, RESUME_SECTIONS


def extract_text(filepath):
    """Extract raw text from a resume file (.pdf, .docx, .txt)."""
    ext = filepath.rsplit(".", 1)[-1].lower()
    text = ""

    if ext == "pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"

    elif ext == "docx":
        import docx
        document = docx.Document(filepath)
        text = "\n".join(p.text for p in document.paragraphs)

    elif ext == "txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    return text


def extract_skills(text):
    """Return the list of skills (from SKILL_BANK) found in the resume text."""
    text_lower = text.lower()
    found = []
    for skill in SKILL_BANK:
        # word-boundary-ish match so "r" doesn't match inside "for"
        pattern = r"(?<![a-zA-Z])" + re.escape(skill) + r"(?![a-zA-Z])"
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(set(found))


def detect_sections(text):
    """Return which standard resume sections appear to be present."""
    text_lower = text.lower()
    return [s for s in RESUME_SECTIONS if s in text_lower]


def score_resume(text):
    """
    Compute a 0-100 resume score using a transparent, explainable rubric:
      - Skills coverage        : up to 40 points
      - Section completeness   : up to 25 points
      - Length / detail        : up to 15 points
      - Contact info present   : up to 10 points
      - Quantified achievements: up to 10 points
    Returns (score, feedback_list, skills_found)
    """
    feedback = []
    skills_found = extract_skills(text)
    sections_found = detect_sections(text)

    # 1. Skills coverage (cap contribution at 20 matched skills)
    skills_score = min(len(skills_found), 20) / 20 * 40
    if len(skills_found) < 5:
        feedback.append("Add more relevant technical skills — only a few were detected.")
    else:
        feedback.append(f"Good skill coverage: {len(skills_found)} relevant skills detected.")

    # 2. Section completeness
    section_score = len(sections_found) / len(RESUME_SECTIONS) * 25
    missing = [s for s in RESUME_SECTIONS if s not in sections_found]
    if missing:
        feedback.append("Consider adding these sections: " + ", ".join(missing[:5]) + ".")

    # 3. Length / detail (word count heuristic)
    word_count = len(text.split())
    if word_count < 150:
        length_score = 5
        feedback.append("Resume seems too short — add more detail about projects/experience.")
    elif word_count > 1200:
        length_score = 10
        feedback.append("Resume is quite long — consider trimming to 1-2 pages of relevant content.")
    else:
        length_score = 15
        feedback.append("Resume length looks appropriate.")

    # 4. Contact info present (email / phone pattern)
    has_email = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text) is not None
    has_phone = re.search(r"(\+?\d[\d\-\s]{8,}\d)", text) is not None
    contact_score = (5 if has_email else 0) + (5 if has_phone else 0)
    if not has_email:
        feedback.append("No email address detected — make sure your contact info is visible.")
    if not has_phone:
        feedback.append("No phone number detected — add one for recruiters to reach you.")

    # 5. Quantified achievements (numbers/percentages near action verbs)
    quantified = len(re.findall(r"\b\d+%|\b\d+\+|\bincreased|\breduced|\bimproved|\bachieved\b", text.lower()))
    achievement_score = min(quantified, 5) / 5 * 10
    if quantified == 0:
        feedback.append("Add quantified achievements (e.g., 'improved performance by 20%').")

    total = round(skills_score + section_score + length_score + contact_score + achievement_score)
    total = max(0, min(100, total))

    if total >= 80:
        feedback.insert(0, "Strong resume overall — well structured and detailed.")
    elif total >= 60:
        feedback.insert(0, "Decent resume, but a few improvements will make it stand out more.")
    else:
        feedback.insert(0, "Resume needs significant improvement before applying to top companies.")

    return total, feedback, skills_found


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
