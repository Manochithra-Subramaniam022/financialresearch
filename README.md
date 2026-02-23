# Research Portal - Financial Data Extractor

A robust Flask web application designed to automatically parse and extract key financial metrics from PDF reports using Gemini AI. It now features a completely secure, full-stack User Authentication system with a sleek SaaS aesthetic.

## Features

- **Full-Stack User Authentication:** Secure sign-up, login, and session management powered by Flask-Login and SQLite.
- **Premium Modern UI:** A beautiful dark-mode interface featuring glassmorphism, smooth animations, and optimized focus transitions.
- **PDF Data Parsing:** Extracts complex data preserving document layout using `pdfplumber`.
- **Gemini AI Integration:** Utilizes Google's Generative AI (`gemini-2.5-flash`) to accurately sift through text and return perfectly structured JSON of financial indicators.

## Setup Instructions

### 1. Requirements

Make sure you have Python 3.10+ installed. Install the dependencies using pip:
```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_google_api_key_here
```

### 3. Initialize the Database

Before running the application for the first time, you must initialize the SQLite database to create the `User` tables. Run the following command in your terminal:

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```
This will generate a `research_portal.db` file in the `instance` folder or root.

### 4. Run the Application

Start the Flask development server:
```bash
python app.py
```

Navigate to `http://127.0.0.1:5000` in your browser. You will be greeted by the Landing Page where you can Create an Account or Log In to access the extraction Dashboard!

## Note on Mock Data
If you don't have a financial PDF report handy, you can generate a mock one by running:
```bash
python create_sample_pdf.py
```
This will create `sample_financial_report.pdf` which can be uploaded to the portal to test the AI data extraction process.
