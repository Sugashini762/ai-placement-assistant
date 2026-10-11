"""
Job <-> Student matching engine.

Computes a match percentage between a student's extracted skill set and a
job's required skills, plus CGPA eligibility, to rank the most relevant
openings for each student (and vice versa for the admin view).
"""


def compute_match_score(student_skills, job_skills):
    """Return an integer 0-100 match score based on skill overlap (Jaccard-ish)."""
    student_set = {s.lower().strip() for s in student_skills}
    job_set = {s.lower().strip() for s in job_skills}

    if not job_set:
        return 0

    overlap = student_set & job_set
    score = round(len(overlap) / len(job_set) * 100)
    return max(0, min(100, score))


def is_eligible(student_cgpa, job_min_cgpa):
    return (student_cgpa or 0) >= (job_min_cgpa or 0)


def rank_jobs_for_student(student_profile, jobs):
    """Return jobs sorted by match score (desc), each annotated with score + eligibility."""
    results = []
    student_skills = student_profile.skills_list()
    for job in jobs:
        if not job.is_active:
            continue
        score = compute_match_score(student_skills, job.skills_list())
        eligible = is_eligible(student_profile.cgpa, job.min_cgpa)
        results.append({
            "job": job,
            "score": score,
            "eligible": eligible,
            "missing_skills": sorted(set(job.skills_list()) - set(student_skills)),
        })
    results.sort(key=lambda r: r["score"], reverse=True)
    return results


def rank_students_for_job(job, student_profiles):
    """Return students sorted by match score (desc) for a given job (admin view)."""
    results = []
    job_skills = job.skills_list()
    for sp in student_profiles:
        score = compute_match_score(sp.skills_list(), job_skills)
        eligible = is_eligible(sp.cgpa, job.min_cgpa)
        results.append({"student": sp, "score": score, "eligible": eligible})
    results.sort(key=lambda r: r["score"], reverse=True)
    return results
