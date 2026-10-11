# A curated list of common technical + soft skills used for keyword matching.
# This acts as the "knowledge base" the AI modules match resumes/jobs against.

SKILL_BANK = [
    # Programming languages
    "python", "java", "c++", "c", "c#", "javascript", "typescript", "go", "golang",
    "rust", "kotlin", "swift", "php", "ruby", "r", "scala", "matlab",
    # Web
    "html", "css", "react", "reactjs", "angular", "vue", "vuejs", "node.js", "nodejs",
    "express", "django", "flask", "fastapi", "spring", "spring boot", "next.js",
    "rest api", "graphql", "bootstrap", "tailwind",
    # Data / AI / ML
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn", "pandas",
    "numpy", "opencv", "data analysis", "data science", "data visualization",
    "power bi", "tableau", "matplotlib", "seaborn", "statistics", "artificial intelligence",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "redis", "oracle", "nosql",
    "firebase",
    # Cloud / DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "jenkins", "ci/cd",
    "git", "github", "gitlab", "linux", "bash", "devops", "terraform",
    # CS fundamentals
    "data structures", "algorithms", "dsa", "oop", "object oriented programming",
    "operating systems", "computer networks", "dbms", "system design",
    # Mobile
    "android", "ios", "flutter", "react native",
    # Soft skills
    "communication", "leadership", "teamwork", "problem solving", "time management",
    "critical thinking", "adaptability", "collaboration", "presentation",
    # Tools
    "excel", "jira", "figma", "postman", "vs code",
]

# Resume sections we look for to judge completeness/structure
RESUME_SECTIONS = [
    "education", "experience", "projects", "skills", "certifications",
    "achievements", "internship", "objective", "summary", "contact",
]

# Ideal keyword sets for common interview questions, used for lightweight
# keyword-coverage scoring of a candidate's free-text answer.
INTERVIEW_QUESTION_BANK = {
    "Software Engineer": [
        {
            "question": "Tell me about yourself and your technical background.",
            "keywords": ["project", "experience", "skill", "developer", "learn", "technology"],
        },
        {
            "question": "Explain the difference between an array and a linked list.",
            "keywords": ["memory", "contiguous", "pointer", "node", "insertion", "access", "index"],
        },
        {
            "question": "What is Object-Oriented Programming? Name its core principles.",
            "keywords": ["encapsulation", "inheritance", "polymorphism", "abstraction", "class", "object"],
        },
        {
            "question": "Describe a challenging project you worked on and how you solved the problem.",
            "keywords": ["challenge", "problem", "solution", "team", "result", "learn"],
        },
        {
            "question": "What is time complexity and why does it matter?",
            "keywords": ["time complexity", "big o", "efficiency", "algorithm", "performance", "scale"],
        },
    ],
    "Data Analyst": [
        {
            "question": "Tell me about yourself and your interest in data analytics.",
            "keywords": ["data", "analysis", "insight", "project", "tool", "experience"],
        },
        {
            "question": "What steps would you take to clean a messy dataset?",
            "keywords": ["missing values", "duplicate", "outlier", "normalize", "clean", "validate"],
        },
        {
            "question": "Explain the difference between SQL JOIN types you know.",
            "keywords": ["inner join", "left join", "right join", "outer join", "table", "key"],
        },
        {
            "question": "How would you present findings to a non-technical stakeholder?",
            "keywords": ["visualization", "chart", "simplify", "story", "dashboard", "summary"],
        },
        {
            "question": "What is the difference between correlation and causation?",
            "keywords": ["correlation", "causation", "relationship", "variable", "experiment", "confound"],
        },
    ],
    "HR / Behavioral": [
        {
            "question": "Why do you want to join our company?",
            "keywords": ["company", "growth", "learn", "value", "opportunity", "culture"],
        },
        {
            "question": "Describe a time you worked in a team to solve a problem.",
            "keywords": ["team", "collaborate", "role", "conflict", "result", "communication"],
        },
        {
            "question": "What are your strengths and weaknesses?",
            "keywords": ["strength", "weakness", "improve", "skill", "self-aware", "work on"],
        },
        {
            "question": "Where do you see yourself in five years?",
            "keywords": ["career", "growth", "goal", "learn", "role", "future"],
        },
        {
            "question": "How do you handle pressure and tight deadlines?",
            "keywords": ["pressure", "deadline", "prioritize", "plan", "calm", "manage"],
        },
    ],
}
