SKILL_CATEGORIES = {

    "Programming Languages": [
        "Python","Java","C","C++","JavaScript"
    ],

    "Web Development": [
        "HTML","CSS","Bootstrap","Flask","Django","React","Node.js"
    ],

    "Database": [
        "SQL","MySQL","MongoDB"
    ],

    "AI / Machine Learning": [
        "Machine Learning",
        "Data Science",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch"
    ],

    "Cloud & DevOps": [
        "Docker",
        "AWS",
        "Git",
        "GitHub"
    ]

}


def extract_skills(text):

    detected = []

    text_lower = text.lower()

    for category in SKILL_CATEGORIES.values():

        for skill in category:

            if skill.lower() in text_lower:
                detected.append(skill)

    return sorted(set(detected))


def categorize_skills(detected_skills):

    categorized = {}

    for category, skills in SKILL_CATEGORIES.items():

        matched = []

        for skill in skills:

            if skill in detected_skills:
                matched.append(skill)

        categorized[category] = matched

    return categorized


def missing_skills(detected_skills):

    missing = []

    for category in SKILL_CATEGORIES.values():

        for skill in category:

            if skill not in detected_skills:
                missing.append(skill)

    return missing