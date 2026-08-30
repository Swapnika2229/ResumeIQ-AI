JOB_ROLE_RULES = {

    "Python Developer": [
        "Python",
        "Flask",
        "SQL",
        "Git"
    ],

    "Backend Developer": [
        "Python",
        "Flask",
        "MySQL",
        "Git",
        "Docker"
    ],

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Bootstrap"
    ],

    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Python",
        "Flask",
        "SQL"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy"
    ]
}


def predict_job_roles(detected_skills):

    predictions = []

    detected = set(detected_skills)

    for role, required in JOB_ROLE_RULES.items():

        matched = len(detected.intersection(required))

        percentage = int((matched / len(required)) * 100)

        predictions.append((role, percentage))

    predictions.sort(key=lambda x: x[1], reverse=True)

    return predictions