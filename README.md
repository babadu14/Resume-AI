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
git clone https://github.com/babadu14/Resume-AI.git
cd Resume-AI

# Set up a virtual environment
python -m venv env
env\Scripts\activate  # On Mac: source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

#create a .env file in your code editor and write the following things:

EMAIL_HOST_USER = "your email"
EMAIL_HOST_PASSWORD = "password"

                        #HOW TO GET PASSWORD 
to get the password go to your email page, gmail is preferable

click on your profile picture in the top right corner and click manage your google account

once there in the search bar type "sign in with app passwords"

scroll down until you find "create and manage your app passwords" button (it should be highlited)

click on it. and enter your password

#after that type in the app name(whatever you want) and click on create, you will see a code. copy it and paste it in the .env file 


#ALL OF THIS IS NECESSARY, OTHERWISE CODE WONT BE SENT TO YOUR EMAIL AND YOU WONT BE ABLE TO LOG IN


# Start the server
python manage.py runserver

## 🔑 Hugging Face Token Setup

This project uses Hugging Face models (e.g., **Google Gemma 2B IT**). To run the app locally, you need a Hugging Face account and an access token.

### Steps:

1. **Create a Hugging Face Account**
   - Go to [https://huggingface.co/join](https://huggingface.co/join) and sign up.

2. **Generate an Access Token**
   - Visit [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Click **New token**, give it a name, and select **Read** permission.
   - Copy the token.

3. **Log in from your terminal**
   ```bash
   huggingface-cli login


```
---

## ⚠️ Usage Limitations

This app is optimized for lightweight resumes (1–2 pages, simple formatting).

Please avoid uploading heavy or overly designed resumes (e.g. CVs with lots of tables, graphics, or 5+ pages).

Large files may lead to long processing times or incomplete AI corrections due to model token limitations.

PDF files should contain real text (not just scanned images) — scanned resumes won't work.

---

## 🧠 Why It Matters

Models like Gemma 2B and others on Hugging Face have context length limits (usually 1024 tokens or less).

Longer resumes get truncated or cause the model to fail or "echo" back the prompt.

Heavy DOCX/PDF resumes with complex formatting may extract poorly, producing messy or unreadable AI results.


