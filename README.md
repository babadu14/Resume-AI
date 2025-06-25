# 📄 Resume-AI

**Resume-AI** is an AI-powered resume grader and editor built with Django, DRF, and Hugging Face. Users can upload their resumes (PDF or DOCX), and the app returns detailed feedback — including grades, soft skill evaluations, and improvement suggestions. Users can also choose to receive an AI-corrected version of their resume.

---

## 🚀 Features

- Upload resumes in PDF or DOCX
- AI-powered resume grading using Google Gemma 2B IT
- Feedback includes:
  - Skills match
  - Grammar and clarity
  - Formatting
  - Soft skills
  - Suggested job titles
- Optional: Get a corrected version of your resume
- JWT authentication

---

## 🛠 Tech Stack

- Python 3.11
- Django + Django Rest Framework
- Hugging Face Transformers
- Google Gemma 2B IT model
- SQLite (for demo)
- Swagger/OpenAPI auto docs

---

## 🔧 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/Resume-AI.git
cd Resume-AI

# Set up a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
