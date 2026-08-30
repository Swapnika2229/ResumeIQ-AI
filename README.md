### AI-Powered Resume Analyzer & Career Coach

ResumeIQ AI is a full-stack Flask web application that analyzes resumes using AI and provides actionable career guidance.

The platform combines resume parsing, skill extraction, ATS scoring, job-role prediction, AI-powered resume review, job matching, interview preparation, resume rewriting, cover-letter generation, career roadmaps, contextual resume chat, and downloadable reports into a single application.

---

# ✨ Features

## 📄 Resume Analysis
- Upload resumes in PDF and DOCX formats
- Extract and clean resume text
- Detect technical and professional skills
- Analyze important resume sections
- Identify strengths and improvement areas

## 🎯 ATS Score
- Generate an ATS-style resume score
- Evaluate resume quality and completeness
- Identify areas that may reduce ATS compatibility
- Provide actionable improvement suggestions

## 🤖 AI Career Coach
- AI-powered resume feedback
- Personalized career recommendations
- Suggested job roles based on resume skills
- Skill-gap identification
- Personalized career roadmap

## 💼 Job Matching
- Match resume skills with relevant job roles
- Identify missing or relevant skills
- Provide role-specific recommendations

## 📝 Resume Rewriter
- Improve resume content
- Rewrite weak sections professionally
- Generate stronger, recruiter-friendly descriptions

## ✉️ Cover Letter Generator
- Generate personalized cover letters
- Use resume information to create relevant content

## 🎤 Interview Preparation
- Generate interview questions based on the candidate's profile
- Support technical and career preparation

## 💬 Resume Chat
- Ask questions about the uploaded resume
- Get AI-generated contextual responses
- Interact with resume information conversationally

## 📊 Resume Strength Dashboard
- Visualize resume performance
- View ATS score and detected skills
- Review resume strengths and weaknesses

## 📑 Reports
- Generate resume analysis reports
- Export analysis information
- Send reports through email functionality

## 👤 Authentication
- User registration
- User login/logout
- Session-based authentication
- User-specific resume history

## 🗂️ Resume History
- Store previous resume analyses
- Track ATS scores
- Track detected skills and job matches
- View previous analysis results

---

# 🏗️ System Architecture


                    ┌──────────────────────┐
                    │      User / Browser  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Flask Web Layer    │
                    │   Routes + Sessions   │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌──────────────┐  ┌─────────────┐
       │  Resume    │   │  AI Analysis │  │   Career    │
       │  Parser    │   │   Pipeline   │  │  Features   │
       └─────┬──────┘   └──────┬───────┘  └──────┬──────┘
             │                 │                  │
             ▼                 ▼                  ▼
       ┌─────────────────────────────────────────────┐
       │              AI Modules                     │
       │                                             │
       │ ATS • Skills • Job Roles • Career Coach     │
       │ Job Match • Interview • Rewriter            │
       │ Cover Letter • Roadmap • Resume Chat        │
       └──────────────────────┬──────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
             ┌─────────────┐     ┌─────────────┐
             │ Groq / LLM  │     │   SQLite    │
             │ AI Service  │     │  Database   │
             └─────────────┘     └─────────────┘
                             
                    ┌─────────────────────┐
                    │ Report / Email Utils │
                    └─────────────────────┘

---

# 🔄 Application Workflow


User
  │
  ▼
Register / Login
  │
  ▼
Upload Resume
  │
  ▼
Resume Parser
  │
  ▼
Text Cleaning & Skill Extraction
  │
  ├──────────────► ATS Score
  │
  ├──────────────► Section Analysis
  │
  ├──────────────► Resume Strength
  │
  ├──────────────► Job Role Prediction
  │
  ├──────────────► Job Matching
  │
  └──────────────► AI Career Analysis
                         │
                         ▼
              Career Recommendations
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
        Interview    Resume       Career
        Questions    Rewrite      Roadmap
             │           │           │
             └───────────┼───────────┘
                         ▼
                   Reports / Chat

---

## 🛠️ Tech Stack

| Category               | Technologies            |
| ---------------------- | ----------------------- |
| Backend                | Python, Flask           |
| Frontend               | HTML5, CSS3, JavaScript |
| UI                     | Bootstrap               |
| AI / LLM               | Groq API                |
| Resume Processing      | PDF/DOCX parsing        |
| Database               | SQLite                  |
| Data Processing        | Python                  |
| Report Generation      | ReportLab               |
| Email                  | SMTP                    |
| Authentication         | Flask sessions          |
| Environment Management | python-dotenv           |
| Version Control        | Git & GitHub            |

---

# 📁 Project Structure

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
│           └── logo.png
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

# ⚙️ Installation
## 1. Clone the repository

*git clone https://github.com/Swapnika2229/ResumeIQ-AI.git*
*cd ResumeIQ-AI*

## 2. Create a virtual environment

Windows:

*python -m venv venv*

Activate it:

venv\Scripts\activate

## 3. Install dependencies

*pip install -r requirements.txt*

## 4. Configure environment variables

Create a .env file in the project root.

*GROQ_API_KEY=your_groq_api_key_here*

Never commit your real API key to GitHub.

## 5. Run the application

*python app.py*

Open the application in your browser:

*http://127.0.0.1:5000*

---

# 🔐 Environment Variables

ResumeIQ AI uses environment variables for sensitive credentials.

Create:

*.env*

Example:

*GROQ_API_KEY=your_groq_api_key_here*

A template is provided in:

*.env.example*

The real .env file is excluded from version control using .gitignore.

---

# 🔌 Application Routes

| Route          | Method     | Purpose                    |
| -------------- | ---------- | -------------------------- |
| `/`            | GET        | Dashboard / home           |
| `/register`    | GET / POST | User registration          |
| `/login`       | GET / POST | User authentication        |
| `/logout`      | GET        | User logout                |
| `/upload`      | GET / POST | Upload and analyze resume  |
| `/analysis`    | GET        | Resume analysis            |
| `/resume-chat` | POST       | Ask questions about resume |
| `/career`      | GET        | Career guidance            |
| `/history`     | GET        | Resume analysis history    |
| `/reports`     | GET        | Resume reports             |
| `/settings`    | GET        | User settings              |
| `/send-report` | POST       | Send report                |

---

# 🗃️ Database Schema

ResumeIQ AI uses SQLite for local persistence.

## Users

Stores registered user information.

| Column     | Type      | Description               |
| ---------- | --------- | ------------------------- |
| id         | INTEGER   | Primary key               |
| name       | TEXT      | User name                 |
| email      | TEXT      | User email                |
| password   | TEXT      | Authentication credential |
| created_at | TIMESTAMP | Account creation time     |

## Resume History

Stores previous resume analysis results.

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

# 🧪 Testing

Before using the application, verify:

User registration works
User login/logout works
Resume upload works
PDF/DOCX parsing works
Skill extraction works
ATS scoring works
AI analysis works with a valid Groq API key
Job-role prediction works
Career recommendations work
Resume chat works
Reports can be generated
Resume history is stored correctly

---

# 🧩 Challenges & Solutions

## 1. Resume Parsing

Challenge: Resumes can have different layouts and formatting.

Solution: Implemented resume text extraction and cleaning utilities to convert uploaded documents into usable text for downstream analysis.

## 2. AI Integration

Challenge: Multiple AI features require consistent communication with the language model.

Solution: Centralized AI interaction through the Groq service module and separated individual AI capabilities into dedicated modules.

## 3. Modular Architecture

Challenge: A resume analyzer can quickly become difficult to maintain when every feature is implemented in one file.

Solution: Organized AI functionality into independent modules for ATS scoring, skill extraction, career coaching, job matching, interview generation, rewriting, roadmap generation, and resume chat.

## 4. Persistent User Data

Challenge: Resume analysis results need to persist between sessions.

Solution: Implemented SQLite database functionality for users and resume analysis history.

## 5. Report Generation

Challenge: Analysis results need to be presented in a reusable format.

Solution: Added dedicated utilities for generating PDF/report output.

---

# 📸 Screenshots

The final documentation will showcase the most important application screens, including:

Dashboard
Resume upload
AI resume analysis
ATS score / resume strength
Career guidance
Resume chat
Reports

---

# 🔮 Future Improvements

Cloud database integration
Production deployment
More advanced ATS evaluation
Support for additional resume formats
Job-board API integration
Real-time job recommendations
Improved authentication and security
User profile customization
Advanced analytics and resume comparison
Automated resume optimization for specific job descriptions
More AI-powered career planning features

---

# 💼 Resume Project Description

ResumeIQ AI — AI-Powered Resume Analyzer & Career Coach

Built a full-stack Flask application that uses AI to analyze resumes, extract skills, generate ATS scores, predict suitable job roles, match candidates to opportunities, provide personalized career guidance, generate interview questions, rewrite resume content, create cover letters, and support contextual resume chat. Implemented modular AI services, SQLite persistence, authentication, report generation, file processing, and a responsive dashboard UI.

Technologies: Python, Flask, HTML, CSS, JavaScript, Bootstrap, SQLite, Groq API, ReportLab

---

# 👩‍💻 Author

Swapnika Mohanty
Computer Science & Engineering Student

GitHub:
https://github.com/Swapnika2229
