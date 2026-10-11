"""
Mock Interview engine.

Picks questions for a chosen role from the curated question bank and scores
free-text answers using keyword-coverage matching. This keeps the project
fully offline (no paid LLM API needed) while still giving meaningful,
explainable feedback — appropriate for an academic demo.
"""

import re

from utils.skill_bank import INTERVIEW_QUESTION_BANK


def get_roles():
    return list(INTERVIEW_QUESTION_BANK.keys())


def get_questions(role):
    return INTERVIEW_QUESTION_BANK.get(role, [])


def score_answer(answer, keywords):
    """Score a single free-text answer 0-10 based on keyword coverage + length."""
    if not answer or not answer.strip():
        return 0, "No answer provided."

    answer_lower = answer.lower()
    matched = [kw for kw in keywords if kw in answer_lower]
    coverage_ratio = len(matched) / len(keywords) if keywords else 0

    word_count = len(answer.split())
    length_bonus = 1 if word_count >= 25 else (0.5 if word_count >= 10 else 0)

    raw_score = coverage_ratio * 9 + length_bonus
    score = round(min(10, raw_score))

    if score >= 8:
        feedback = "Excellent answer — covers the key points clearly."
    elif score >= 5:
        feedback = "Good attempt, but you could mention: " + ", ".join(
            [k for k in keywords if k not in matched][:3]
        ) + "."
    else:
        feedback = "Answer needs more depth. Try to include concepts like: " + ", ".join(
            [k for k in keywords if k not in matched][:3]
        ) + "."

    return score, feedback


def evaluate_session(questions, answers):
    """
    questions: list of {question, keywords}
    answers: list of strings (same order/length as questions)
    Returns: (qa_results list, overall_score int 0-100)
    """
    qa_results = []
    total = 0
    for q, ans in zip(questions, answers):
        score, feedback = score_answer(ans, q["keywords"])
        qa_results.append({
            "question": q["question"],
            "answer": ans,
            "score": score,
            "feedback": feedback,
        })
        total += score

    max_possible = len(questions) * 10
    overall = round((total / max_possible) * 100) if max_possible else 0
    return qa_results, overall
