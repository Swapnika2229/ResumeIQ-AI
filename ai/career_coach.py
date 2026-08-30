def generate_career_advice(detected_skills):

    advice = []

    skills = [skill.lower() for skill in detected_skills]

    # Python Developer
    if "python" in skills:
        advice.append("✔ Learn Django or FastAPI for backend development.")
        advice.append("✔ Build REST APIs.")
        advice.append("✔ Learn Docker and deployment.")

    # Web Development
    if "html" in skills and "css" in skills:
        advice.append("✔ Learn JavaScript deeply.")
        advice.append("✔ Learn React.js.")
        advice.append("✔ Build Full Stack Projects.")

    # Database
    if "mysql" in skills or "sql" in skills:
        advice.append("✔ Practice SQL queries daily.")
        advice.append("✔ Learn Database Optimization.")

    # Machine Learning
    if "machine learning" in skills:
        advice.append("✔ Learn Deep Learning.")
        advice.append("✔ Learn TensorFlow.")
        advice.append("✔ Build Computer Vision projects.")

    # Git
    if "git" in skills:
        advice.append("✔ Contribute to Open Source Projects.")

    # Beginner
    if len(detected_skills) < 5:
        advice.append("✔ Improve your technical skills by building more projects.")
        advice.append("✔ Add internships and certifications.")

    if len(advice) == 0:
        advice.append("✔ Start with Python.")
        advice.append("✔ Learn HTML, CSS and JavaScript.")
        advice.append("✔ Build projects regularly.")

    return advice