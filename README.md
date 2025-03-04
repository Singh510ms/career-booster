# Career Booster - AI-Powered Portfolio Project Generator

A web application that uses CrewAI to generate tailored project ideas and platform-specific prompts based on your resume and job descriptions.

## Features

- **Upload your resume**: We analyze your skills and experiences
- **Provide a job posting URL**: We extract key requirements
- **Get project ideas**: Tailored project suggestions that showcase your skills
- **Get platform prompts**: Ready-to-use prompts for Lovable.dev, Bolt.new, and Replit

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Singh510ms/career-booster.git
   cd career-booster
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API key:
   ```
   CEREBRAS_API_KEY=your_cerebras_api_key_here
   ```

## Running the Application

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Upload your resume (PDF) and provide a job posting URL.

4. Wait for the CrewAI agents to analyze your information and generate results.

5. View your tailored project ideas and platform prompts.

## Architecture

- **Frontend**: Flask web application with HTML, CSS, and JavaScript
- **Backend**: CrewAI-powered agents for analyzing resumes and job postings
- **Integration**: Seamless connection between the web interface and CrewAI

## Technologies Used

- Flask
- CrewAI
- Cerebras LLMs
- JavaScript
- HTML/CSS
