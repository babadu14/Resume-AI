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

---

⚠️ Usage Limitations
This app is optimized for lightweight resumes (1–2 pages, simple formatting).

Please avoid uploading heavy or overly designed resumes (e.g. CVs with lots of tables, graphics, or 5+ pages).

Large files may lead to long processing times or incomplete AI corrections due to model token limitations.

PDF files should contain real text (not just scanned images) — scanned resumes won't work.

🧠 Why It Matters
Models like Gemma 2B and others on Hugging Face have context length limits (usually 1024 tokens or less).

Longer resumes get truncated or cause the model to fail or "echo" back the prompt.

Heavy DOCX/PDF resumes with complex formatting may extract poorly, producing messy or unreadable AI results.


