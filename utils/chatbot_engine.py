"""
Placement Chatbot engine.

A lightweight, fully-offline rule-based assistant that answers common
placement queries (eligibility, process, dates, resume tips, companies
visiting, etc.) using intent keyword matching + live data from the database
(jobs, notices). This avoids needing a paid LLM API key while still feeling
like an "AI assistant" for the demo.
"""

import difflib

INTENTS = {
    "greeting": ["hi", "hello", "hey", "good morning", "good evening"],
    "eligibility": ["eligibility", "eligible", "criteria", "cgpa required", "who can apply"],
    "process": ["process", "how does placement work", "steps", "procedure", "how to apply"],
    "companies": ["companies", "which companies", "recruiters", "who is coming", "visiting"],
    "dates": ["date", "schedule", "when", "deadline", "drive date"],
    "resume_tips": ["resume", "cv tips", "improve resume", "resume score"],
    "interview_tips": ["interview", "mock interview", "interview tips", "how to prepare"],
    "contact": ["contact", "placement cell", "coordinator", "email", "phone number"],
    "thanks": ["thank", "thanks", "thank you"],
    "bye": ["bye", "goodbye", "see you"],
}

RESPONSES = {
    "greeting": "Hi! I'm your Placement Assistant. Ask me about eligibility, the placement process, upcoming drives, or resume tips.",
    "eligibility": "Eligibility depends on the company's job posting — check the minimum CGPA and required skills on the Jobs page. Generally, no active backlogs and a minimum CGPA (varies per company) are required.",
    "process": "The placement process typically involves: 1) Registering & completing your profile, 2) Uploading your resume for scoring, 3) Applying to matching jobs, 4) Shortlisting by the company, 5) Interview rounds, 6) Final selection. You can track your applications from your dashboard.",
    "companies": "You can see all currently active job openings and the companies hiring on the 'Browse Jobs' page in your dashboard.",
    "dates": "Drive dates are listed on each job posting under 'Browse Jobs'. Check the Notices section on your dashboard for the latest announcements from the placement cell.",
    "resume_tips": "Use the 'Resume Analysis' tool to get an instant score and feedback. In general: include a skills section, quantify achievements, keep it to 1-2 pages, and make sure your contact info is visible.",
    "interview_tips": "Try the 'Mock Interview' module to practice role-specific questions and get instant feedback. Focus on clear structure (situation-task-action-result) for behavioral questions.",
    "contact": "You can reach the placement cell through the contact details published on the college placement notice board / official website.",
    "thanks": "You're welcome! Good luck with your placements!",
    "bye": "Goodbye! Feel free to come back anytime you have placement-related questions.",
    "fallback": "I'm not sure I understood that. You can ask me about: eligibility, the placement process, companies visiting, important dates, resume tips, or interview tips.",
}


def _match_intent(message):
    message_lower = message.lower().strip()

    # 1. direct substring match
    for intent, keywords in INTENTS.items():
        for kw in keywords:
            if kw in message_lower:
                return intent

    # 2. fuzzy match fallback (handles typos)
    all_keywords = [(kw, intent) for intent, kws in INTENTS.items() for kw in kws]
    best_ratio = 0
    best_intent = None
    for kw, intent in all_keywords:
        ratio = difflib.SequenceMatcher(None, message_lower, kw).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_intent = intent

    if best_ratio > 0.6:
        return best_intent

    return None


def get_response(message, active_jobs_count=None, latest_notice=None):
    intent = _match_intent(message)

    if intent is None:
        return RESPONSES["fallback"]

    response = RESPONSES[intent]

    # Enrich certain intents with live data if provided
    if intent == "companies" and active_jobs_count is not None:
        response += f" Right now there are {active_jobs_count} active job openings."
    if intent == "dates" and latest_notice:
        response += f" Latest notice: \"{latest_notice}\""

    return response
