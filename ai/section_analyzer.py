# ai/section_analyzer.py

SECTIONS = {
    "Contact Information": ["@", "phone", "mobile"],
    "Education": ["education", "b.tech", "bachelor", "degree"],
    "Skills": ["skills"],
    "Projects": ["project", "projects"],
    "Experience": ["experience", "internship"],
    "Certifications": ["certification", "certifications"],
    "Achievements": ["achievement", "achievements"],
    "Languages": ["languages"],
    "Hobbies": ["hobbies", "interests"]
}


def analyze_sections(text):

    text = text.lower()

    report = {}

    for section, keywords in SECTIONS.items():

        found = False

        for keyword in keywords:

            if keyword in text:
                found = True
                break

        report[section] = found

    return report