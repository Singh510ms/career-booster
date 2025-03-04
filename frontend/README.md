# Career Booster Frontend

A simple, modern web interface for the Career Booster tool that generates project ideas and platform-specific prompts based on a resume and job description.

## Features

- Upload resume (PDF format)
- Provide job posting URL
- Generate tailored project ideas
- Get platform-specific prompts for Lovable, Bolt, and Replit

## Requirements

- Python 3.2+
- Flask
- CrewAI backend

## Installation

1. Make sure you have Python installed on your system.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Ensure you have a `.env` file with the required API keys:

```
CEREBRAS_API_KEY=your_cerebras_api_key
```

## How to Run

From the root directory of the project, run:

```bash
cd frontend
python app.py
```

This will start the Flask development server on http://127.0.0.1:5001.

## Usage

1. Open your web browser and navigate to http://127.0.0.1:5001
2. Upload your resume in PDF format
3. Enter the URL of a job posting
4. Click "Generate Project Ideas"
5. Wait for the AI to analyze your resume and the job posting
6. View the generated project ideas and platform-specific prompts

## Project Structure

```
frontend/
├── app.py                 # Flask application
├── static/                # Static assets
│   ├── css/               # CSS stylesheets
│   │   └── style.css      # Custom styles
│   └── js/                # JavaScript files
│       ├── processing.js  # Processing page functionality
│       └── results.js     # Results page functionality
├── templates/             # HTML templates
│   ├── index.html         # Homepage with upload form
│   ├── processing.html    # Processing indicator page
│   └── results.html       # Results display page
└── uploads/               # Directory for uploaded resumes
```

## Notes

- This frontend is designed to work with the CrewAI backend located in `crewai_project/career_booster/src`
- The application uses session storage to maintain state between pages
- Uploaded resumes are stored temporarily and cleared when starting a new session 