# AI Resume Voice Agent

AI Resume Voice Agent is an AI-powered application that helps recruiters quickly retrieve information from candidate resumes using voice.

Instead of manually opening resumes and searching for information, a recruiter can upload a resume PDF and ask questions such as:

- What are Darshan's skills?
- What is Chethan's experience?
- What projects has Rahul worked on?
- What is Priya's email?
- What is the candidate's phone number?

The system understands the recruiter's question, identifies the candidate and requested information, and retrieves the actual data stored in SQLite.

## 🚀 Project Overview

The application combines resume processing, voice recognition, AI-based query understanding, and database retrieval.

The main workflow is:

Resume PDF
↓
FastAPI Upload API
↓
PyMuPDF Text Extraction
↓
Resume Section Parsing
↓
SQLite Database
↓
Voice Input
↓
Speech-to-Text
↓
Ollama llama3.2
↓
Candidate + Requested Section
↓
SQLite Retrieval
↓
Actual Resume Answer
↓
React UI
↓
Text-to-Speech (Future)

## 🧠 Important Architecture

Ollama is used only to understand the user's question.

Ollama does NOT generate or invent resume information.

For example:

User:
"What are Darshan's skills?"

Ollama identifies:

candidate_name = Darshan
requested_section = skills

Then the application retrieves the actual skills from SQLite.

The architecture is:

Ollama → Understand the question
SQLite → Provide the actual answer

This helps prevent the AI from fabricating candidate information.

## 🛠️ Technologies Used

### Backend

- Python 3.13.7
- FastAPI
- SQLite
- PyMuPDF
- Ollama
- Llama 3.2
- OpenAI Whisper
- SoundDevice
- SciPy
- FFmpeg

### Frontend

- React
- Vite
- JavaScript
- HTML
- CSS
- Browser Speech Recognition API

## 📂 Project Structure

AI-Resume-Voice-Agent/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── resume_routes.py
│   │   │   ├── retrieval_routes.py
│   │   │   ├── query_routes.py
│   │   │   └── voice_routes.py
│   │   ├── services/
│   │   │   ├── pdf_service.py
│   │   │   ├── ollama_service.py
│   │   │   └── whisper_service.py
│   │   ├── utils/
│   │   │   └── section_parser.py
│   │   ├── database/
│   │   │   └── database.py
│   │   └── repositories/
│   │       └── resume_repository.py
│   │
│   ├── uploads/
│   ├── voice_uploads/
│   ├── venv/
│   ├── run.py
│   ├── test_parser.py
│   ├── test_database.py
│   ├── test_ollama.py
│   ├── test_whisper.py
│   └── test_transcription.py
│
├── database/
│   └── resumes.db
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md

## 📄 Resume Processing

When a recruiter uploads a PDF resume, the application performs the following steps:

1. Save the uploaded PDF.
2. Extract text using PyMuPDF.
3. Extract the candidate name.
4. Extract email.
5. Extract phone number.
6. Detect resume sections.
7. Store the extracted information in SQLite.

Currently supported resume information includes:

- Candidate Name
- Email
- Phone
- Career Objective
- Skills
- Education
- Experience
- Projects
- Certifications

## 🎤 Voice Query

The recruiter can use the browser microphone instead of manually typing questions.

For example:

"What are Darshan's skills?"

The browser converts the speech into text and sends the query to the FastAPI backend.

The flow is:

Browser Microphone
↓
Speech Recognition
↓
Text Query
↓
FastAPI
↓
Ollama
↓
SQLite
↓
Actual Answer
↓
React Interface

## 🗄️ Database

SQLite is used to store candidate resume information.

The `resumes` table contains:

- id
- candidate_name
- email
- phone
- filename
- career_objective
- skills
- education
- experience
- projects
- certifications

The database acts as the source of truth for candidate information.

## 🔌 API Endpoints

### Upload Resume

POST /resumes/upload

Uploads and processes a PDF resume.

### Retrieve Resume

GET /resumes/{candidate_name}

Retrieves resume information for a candidate.

### Query Resume

POST /query/

Processes natural-language questions about resumes.

### Voice Query

POST /voice/query

Handles voice-based resume query processing and testing.

## ⚙️ Installation

Clone the repository:

git clone https://github.com/YOUR-USERNAME/AI-Resume-Voice-Agent.git

Go into the project:

cd AI-Resume-Voice-Agent

## 🐍 Backend Setup

Go to the backend directory:

cd backend

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

## 🤖 Ollama Setup

Install Ollama and verify it:

ollama --version

Download the model:

ollama pull llama3.2

Test the model:

ollama run llama3.2

## 🎙️ Whisper Setup

Whisper is used for speech-to-text functionality.

The project also uses:

- sounddevice
- scipy
- FFmpeg

Make sure the microphone is available on your system.

## ▶️ Run Backend

From the backend directory:

.\venv\Scripts\Activate.ps1

python run.py

FastAPI normally runs at:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

## ⚛️ Run Frontend

Open another terminal.

Go to the frontend:

cd frontend

Install dependencies:

npm install

Start the React development server:

npm run dev

The frontend normally runs at:

http://localhost:5173

## 🧪 Example

A recruiter uploads:

Darshan_Resume.pdf

Then asks:

"What are Darshan's skills?"

The system processes the question and retrieves the actual information stored in SQLite.

Example response:

Java, Python, JavaScript, SQL, React.js, Spring Boot, MySQL

The answer comes from the database, not from AI-generated resume information.

## 🔒 Data Accuracy

The project follows an important rule:

AI understands the question.
Database provides the answer.

Ollama is not used to invent candidate skills, experience, education, projects, or contact information.

This makes the system more reliable for resume information retrieval.

## 🚧 Future Improvements

- Text-to-Speech responses
- Better resume section detection
- Support for more resume formats
- Candidate comparison
- Recruiter dashboard
- Candidate ranking
- Authentication
- Multiple recruiter accounts
- Conversation history
- Better voice interaction
- Cloud deployment

## 🎯 Use Case

This project is designed for recruiters and HR teams who need to quickly search through multiple candidate resumes.

Instead of manually opening resumes, recruiters can upload resumes once and ask questions naturally using their voice.

Examples:

"What are Rahul's technical skills?"

"Tell me about Priya's experience."

"What projects has Darshan worked on?"

"What is Chethan's email?"

## 👨‍💻 Author

Chethan G

AI Resume Voice Agent built using Python, FastAPI, React, SQLite, Ollama, and Whisper.