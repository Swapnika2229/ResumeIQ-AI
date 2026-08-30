### AI-Powered Resume Analyzer & Career Coach

ResumeIQ AI is a full-stack AI-powered web application that analyzes resumes, evaluates ATS compatibility, identifies skills, recommends suitable job roles, generates personalized career guidance, and provides an interactive AI assistant that answers questions based specifically on the user's resume.

The application combines resume parsing, Natural Language Processing, machine learning, AI-powered analysis, database persistence, and a modern web dashboard into a single career-focused platform.

---

## 🎯 Problem Statement

Job seekers often struggle to understand:

- Whether their resume is ATS-friendly
- Which skills are already strong
- Which skills are missing
- Which job roles match their profile
- How to improve their resume
- How to prepare for interviews
- What career path they should follow

ResumeIQ AI brings these capabilities together in one application and provides personalized recommendations based on the user's resume.

---

# ✨ Features

## 📄 Resume Analysis

Upload a PDF or DOCX resume and automatically extract its content for analysis.

The system analyzes:

- Resume text
- Skills
- Skill categories
- Resume sections
- ATS compatibility
- Missing skills
- Resume strengths
- Improvement areas

---

## 🎯 ATS Score

ResumeIQ AI evaluates the resume and generates an ATS-oriented score.

It provides actionable suggestions to improve:

- Keywords
- Skills
- Resume structure
- Content quality
- Job relevance

---

## 🧠 AI Resume Review

The application uses an AI service to provide personalized resume feedback.

The AI reviews the extracted resume and generates recommendations for improving the candidate's profile.

---

## 💼 Job Role Prediction

Based on detected skills and resume content, ResumeIQ AI identifies suitable career/job roles.

Examples include:

- Software Developer
- Data Analyst
- Machine Learning Engineer
- Backend Developer
- Frontend Developer
- Data Scientist

---

## 🔍 Job Match

Users can provide a job description and compare it against their resume.

The system evaluates how well the resume matches the target position.

---

## 💬 Chat With Your Resume

ResumeIQ AI includes an interactive AI assistant that allows users to ask questions about their own resume.

Example:

> What are my strongest skills?

> Which skills should I improve?

> Am I suitable for a software developer role?

The assistant uses the user's extracted resume content to generate contextual answers.

---

## 🎤 Interview Question Generator

Generate interview questions based on the candidate's resume.

This helps users prepare for interviews using their actual skills and experience.

---

## ✍️ Resume Rewriter

Generate improved versions of resume content with AI assistance.

The feature focuses on making resume content clearer, stronger, and more professional.

---

## 📝 Cover Letter Generator

Generate a personalized cover letter based on the user's resume.

---

## 🗺️ Career Roadmap

ResumeIQ AI provides a career roadmap based on the user's detected skills and profile.

The roadmap helps identify:

- Current skills
- Skills to learn
- Career direction
- Suggested development areas

---

## 📊 Resume Strength Analysis

The system evaluates different aspects of the resume and provides an overall assessment of resume strength.

---

## 📑 Resume Reports

Generate a structured resume analysis report containing important results and recommendations.

---

## 📧 Report Sharing

The application includes functionality to send generated reports through email.

---

## 👤 User Authentication

ResumeIQ AI includes:

- User registration
- User login
- Password hashing
- Session-based authentication
- User-specific resume history

---

## 🗃️ Resume History

Resume analysis records are stored in SQLite so users can maintain their resume analysis history.

---

## 🏗️ System Architecture


                         ┌─────────────────────┐
                         │      User           │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Flask Web App     │
                         │      app.py         │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
      │ Resume Parser │     │ AI Processing │     │   Database    │
      │               │     │               │     │    SQLite     │
      └───────┬───────┘     └───────┬───────┘     └───────────────┘
              │                     │
              ▼                     ▼
      ┌───────────────┐     ┌───────────────────┐
      │ Extracted     │     │ Groq AI Service   │
      │ Resume Text   │     │                   │
      └───────┬───────┘     └─────────┬─────────┘
              │                       │
              └───────────┬───────────┘
                          ▼
                ┌─────────────────────┐
                │ Resume Intelligence │
                │ & Recommendations   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Dashboard / Reports │
                └─────────────────────┘

---

# 🧩 Project Architecture

The application is organized into separate modules for better maintainability.

ResumeIQ-AI/
│
├── ai/
│   ├── analyzer.py
│   ├── ats_score.py
│   ├── career_coach.py
│   ├── cover_letter.py
│   ├── groq_service.py
│   ├── interview_generator.py
│   ├── job_match.py
│   ├── job_roles.py
│   ├── resume_chat.py
│   ├── resume_parser.py
│   ├── resume_rewriter.py
│   ├── resume_strength.py
│   ├── roadmap_generator.py
│   ├── section_analyzer.py
│   └── skill_extractor.py
│
├── database/
│   └── database.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── branding/
│
├── templates/
│   ├── components/
│   │   └── sidebar.html
│   ├── analysis.html
│   ├── base.html
│   ├── career.html
│   ├── dashboard.html
│   ├── dashboard_base.html
│   ├── history.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── reports.html
│   ├── settings.html
│   └── upload.html
│
├── utils/
│   ├── email_sender.py
│   ├── file_handler.py
│   ├── pdf_generator.py
│   ├── report_generator.py
│   └── text_cleaner.py
│
├── app.py
├── email_config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

---

# 🛠️ Tech Stack

## Backend

Python
Flask
SQLite
Werkzeug

## AI / Machine Learning

Groq API
scikit-learn
Natural Language Processing
Resume text analysis
Skill extraction

## Frontend

HTML5
CSS3
JavaScript
Bootstrap 5

## Document Processing
 
PDF processing
DOCX processing
Report generation

## Database

SQLite
Python SQLite3

## Development Tools

Git
GitHub
Python Virtual Environment

---

# 🔄 Application Workflow

1. User Registration / Login
              ↓
2. Upload Resume
              ↓
3. Resume File Validation
              ↓
4. Resume Text Extraction
              ↓
5. Skill Extraction
              ↓
6. Resume Section Analysis
              ↓
7. ATS Score Calculation
              ↓
8. Job Role Prediction
              ↓
9. Job Matching
              ↓
10. AI Resume Review
              ↓
11. Career Recommendations
              ↓
12. Interview Questions
              ↓
13. Resume Rewriting
              ↓
14. Cover Letter Generation
              ↓
15. Career Roadmap
              ↓
16. Resume Chat
              ↓
17. Report Generation

---

# 🗃️ Database Schema

ResumeIQ AI currently uses SQLite.

## Users

Stores registered user information.

| Column   | Type    | Description      |
| -------- | ------- | ---------------- |
| id       | INTEGER | Primary key      |
| fullname | TEXT    | User's full name |
| email    | TEXT    | User email       |
| password | TEXT    | Hashed password  |


## Resume History

Stores resume analysis history.

| Column        | Type      | Description               |
| ------------- | --------- | ------------------------- |
| id            | INTEGER   | Primary key               |
| user_id       | INTEGER   | Associated user           |
| filename      | TEXT      | Uploaded resume filename  |
| ats_score     | INTEGER   | ATS score                 |
| skills_count  | INTEGER   | Number of detected skills |
| job_matches   | INTEGER   | Job matching result       |
| resume_rating | TEXT      | Resume rating             |
| upload_date   | TIMESTAMP | Upload timestamp          |

---

# 🔌 Application Routes

The Flask application contains routes for authentication, resume processing, analysis, career guidance, reports, and resume chat.

| Route          | Method   | Purpose                    |
| -------------- | -------- | -------------------------- |
| `/`            | GET      | Dashboard                  |
| `/register`    | GET/POST | User registration          |
| `/login`       | GET/POST | User login                 |
| `/logout`      | GET      | User logout                |
| `/upload`      | GET/POST | Upload and analyze resume  |
| `/analysis`    | GET      | AI resume analysis         |
| `/resume-chat` | POST     | Ask questions about resume |
| `/career`      | GET      | Career guidance            |
| `/history`     | GET      | Resume history             |
| `/reports`     | GET      | Resume reports             |
| `/settings`    | GET      | User settings              |
| `/send-report` | POST     | Send report                |

---

# 🔐 Environment Variables

API credentials are not stored in the repository.

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

The repository contains .env.example as a safe template.

Never commit your actual .env file or API keys to GitHub.

---

# ⚙️ Installation
## 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ResumeIQ-AI.git
cd ResumeIQ-AI

## 2. Create a virtual environment
Windows
python -m venv venv
Activate it
venv\Scripts\Activate.ps1

## 3. Install dependencies
pip install -r requirements.txt

## 4. Configure environment variables
Create .env:
GROQ_API_KEY=your_groq_api_key_here

## 5. Run the application
python app.py
Open:
http://127.0.0.1:5000

---

# 🧪 Testing

The application was tested through the complete resume analysis workflow:

User Login
    ↓
Resume Upload
    ↓
Resume Parsing
    ↓
AI Analysis
    ↓
ATS Scoring
    ↓
Skill Detection
    ↓
Job Matching
    ↓
Career Analysis
    ↓
Resume Chat
    ↓
Report Generation

The Resume Chat feature uses the stored resume data so that questions can be answered using the uploaded resume.

---

# 🧠 AI Resume Chat

One of the key features of ResumeIQ AI is contextual resume-based conversation.

Instead of treating the AI assistant as a generic chatbot, the application passes the user's extracted resume content together with the user's question.

Example:

Resume:
[Extracted resume content]

Question:
   What are my strongest skills?

                ↓

            AI Analysis

                ↓

      Personalized Response

This allows the assistant to provide answers grounded in the candidate's resume.

---

# 🧩 Challenges & Solutions
## 1. Resume Text Persistence

*Challenge*

Large resume text should not be stored inside Flask's client-side session cookie because browser cookies have size limitations.

*Solution*

Resume data was moved to a database-backed persistence approach so that the application can maintain resume information without unnecessarily increasing the session cookie size.

## 2. Resume Chat Context

*Challenge*

The AI resume chat initially returned:

No resume is currently loaded.

because the resume content was not reliably available when the chat request was made.

*Solution*

The resume data flow was redesigned so the chat feature retrieves the appropriate resume content before sending the request to the AI service.

## 3. Resume File Processing

*Challenge*

Uploaded resumes can contain different formatting and document structures.

*Solution*

The application separates file handling, text extraction, cleaning, and analysis into dedicated modules.

## 4. AI Service Integration

*Challenge*

AI-powered features depend on an external API and therefore need secure credential handling and error handling.

*Solution*

The project uses environment variables for API credentials and isolates AI communication inside a dedicated Groq service module.

## 5. Modular Architecture

*Challenge*

A resume analysis platform contains many independent features.

*Solution*

AI functionality was separated into individual modules such as:

ATS scoring
Skill extraction
Job matching
Career coaching
Resume chat
Resume rewriting
Interview generation
Career roadmap

This makes the application easier to maintain and extend.

---

# 🔮 Future Improvements

Potential future improvements include:

Cloud database integration
Production deployment
PostgreSQL support
User profile management
More advanced ATS scoring
Job-board API integration
Personalized job recommendations
Resume version comparison
Resume improvement tracking
Authentication improvements
Background processing for large resumes
Automated resume-to-job optimization
More advanced NLP models
Analytics dashboard
Docker deployment
Automated testing and CI/CD
Mobile-responsive improvements

---

# 📸 Screenshots

Screenshots of the application will be added here.

Planned screenshots:

Landing page
Login / Registration
Dashboard
Resume upload
AI analysis
ATS score
Skills analysis
Career roadmap
Resume chat
Reports
Resume history

---

# 💼 Resume Project Description

*ResumeIQ AI — AI Resume Analyzer & Career Coach*

Developed a full-stack Flask-based AI resume analysis platform that parses PDF/DOCX resumes, extracts skills, evaluates ATS compatibility, predicts suitable job roles, performs job matching, generates AI-powered resume feedback, creates interview questions and career roadmaps, and provides contextual resume-based chat. Implemented SQLite persistence, modular AI services, report generation, authentication, and a responsive Bootstrap dashboard.

*Key Technologies*

Python · Flask · SQLite · Groq API · scikit-learn · NLP · HTML · CSS · JavaScript · Bootstrap · Git

---

# 📈 Project Highlights

Full-stack AI-powered application
Modular Python architecture
Resume parsing and NLP-based skill extraction
ATS-oriented resume evaluation
AI-powered career guidance
Job matching
Context-aware resume chatbot
Interview preparation
Resume rewriting
Cover letter generation
Career roadmap generation
PDF report generation
User authentication
Resume history persistence
Environment-based API key management

---

# 👩‍💻 Author

Swapnika Mohanty
B.Tech — Computer Science & Engineering
