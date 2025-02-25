#!/usr/bin/env python3
"""
Career Booster - Web Application
A SaaS-based frontend for the Career Booster multi-agent system.
"""

import os
import json
import uuid
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import markdown

from agents import CareerBoosterAgents
from parsers import parse_resume_pdf, fetch_job_posting, save_temp_pdf
from prompt_generator import (
    generate_v0_prompt,
    generate_lovable_prompt,
    generate_replit_prompt,
    generate_generic_prompt
)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            static_folder='frontend/static',
            template_folder='frontend/templates')
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Add this near the top of the file, after imports
TEST_MODE = True  # Set to False when ready for production

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def md_to_html(text):
    """Convert markdown to HTML"""
    if not text:
        return ""
    return markdown.markdown(text, extensions=['fenced_code', 'tables'])

app.jinja_env.filters['markdown'] = md_to_html

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """Process the uploaded resume and job posting URL."""
    try:
        # Check if the post request has the file part
        if 'resume' not in request.files:
            flash('No resume file uploaded')
            return redirect(url_for('index'))
        
        file = request.files['resume']
        job_url = request.form.get('job_url', '')
        
        # Get API keys from environment variables instead of form
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        cerebras_api_key = os.environ.get('CEREBRAS_API_KEY')
        
        # Save API keys to session (optional, for later use)
        session['openai_api_key'] = openai_api_key
        session['cerebras_api_key'] = cerebras_api_key
        
        # If user did not select a file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No resume file selected')
            return redirect(url_for('index'))
        
        if not job_url:
            flash('No job posting URL provided')
            return redirect(url_for('index'))
        
        # Validate API key
        if not openai_api_key:
            flash('OpenAI API key is missing in environment variables')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Store file path and job URL in session
            session['resume_path'] = file_path
            session['job_url'] = job_url
            
            # Return success response for AJAX request
            return jsonify({'status': 'success', 'message': 'File uploaded successfully'})
        
        flash('Invalid file type. Please upload a PDF file.')
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error processing upload: {e}")
        flash(f'Error processing upload: {str(e)}')
        return redirect(url_for('index'))

@app.route('/processing')
def processing():
    """Render the processing page."""
    return render_template('processing.html')

@app.route('/generate_results', methods=['GET'])
def generate_results():
    """Generate results using the CrewAI agents or test data."""
    try:
        # Add debug logging
        logger.info(f"Session data: {session}")
        
        # Get paths from session
        resume_path = session.get('resume_path')
        job_url = session.get('job_url')
        
        if not resume_path or not job_url:
            return jsonify({
                'status': 'error',
                'message': 'Missing required information. Please try again.'
            })
            
        if TEST_MODE:
            # Create sample data for testing instead of using CrewAI
            logger.info("Using test mode with sample data")
            job_posting = fetch_job_posting(job_url)  # Still fetch the real job posting
            
            project_ideas = """
# Project Ideas Based on Your Resume and the Job Posting

## 1. Full-Stack E-commerce Dashboard

Create a comprehensive e-commerce analytics dashboard that allows store owners to track sales, inventory, customer behavior, and marketing campaign performance in real-time.

**Technologies**: React, Node.js, Express, MongoDB, Chart.js
**Key Features**:
- Real-time sales and inventory tracking
- Customer behavior analytics
- Marketing campaign performance metrics
- Customizable dashboard widgets
- Data export and reporting

## 2. AI-Powered Content Recommendation System

Build a content recommendation system that uses machine learning to suggest relevant articles, products, or media based on user behavior and preferences.
"""
            roadmap = """
# Project Roadmap: Full-Stack E-commerce Dashboard

## Week 1: Planning and Setup

### Day 1-2: Project Planning
- Define project scope and requirements
- Create wireframes and mockups
- Set up project repository and documentation
- Choose specific technologies and libraries

### Day 3-4: Environment Setup
- Set up development environment
- Initialize frontend React application
- Initialize backend Node.js/Express application
- Set up MongoDB database
- Configure basic authentication
"""
        else:
            # Parse resume and job posting
            resume_text = parse_resume_pdf(resume_path)
            job_posting = fetch_job_posting(job_url)
            
            # Initialize agents
            career_booster = CareerBoosterAgents()
            crew = career_booster.create_crew()
            
            # Set job data as environment variables for the crew
            os.environ["JOB_DESCRIPTION"] = job_posting
            os.environ["CANDIDATE_RESUME"] = resume_text
            
            # Run the crew without the inputs parameter
            result = crew.kickoff()
            
            # Parse the results
            project_ideas = result.get("project_ideas", "No project ideas generated")
            roadmap = result.get("roadmap", "No roadmap generated")
        
        # Store results in session
        session['job_analysis'] = job_posting
        session['project_ideas'] = project_ideas
        session['roadmap'] = roadmap
        
        # Generate prompts
        v0_prompt = generate_v0_prompt(project_ideas, roadmap)
        lovable_prompt = generate_lovable_prompt(project_ideas, roadmap)
        replit_prompt = generate_replit_prompt(project_ideas, roadmap)
        generic_prompt = generate_generic_prompt(project_ideas, roadmap)
        
        # Store prompts in session
        session['prompts'] = {
            'v0': v0_prompt,
            'lovable': lovable_prompt,
            'replit': replit_prompt,
            'generic': generic_prompt
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Results generated successfully'
        })
    
    except Exception as e:
        logger.error(f"Error generating results: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Error generating results: {str(e)}'
        })

@app.route('/results')
def results():
    """Render the results page."""
    job_analysis = session.get('job_analysis', '')
    project_ideas = session.get('project_ideas', '')
    roadmap = session.get('roadmap', '')
    prompts = session.get('prompts', {})
    
    return render_template('results.html',
                          job_analysis=job_analysis,
                          project_ideas=project_ideas,
                          roadmap=roadmap,
                          prompts=prompts)

@app.route('/download/<platform>')
def download_prompt(platform):
    """Download a prompt file."""
    prompts = session.get('prompts', {})
    
    if platform not in prompts:
        flash(f'No prompt file found for {platform}')
        return redirect(url_for('results'))
    
    content = prompts.get(platform, '')
    
    return content, 200, {
        'Content-Type': 'text/markdown',
        'Content-Disposition': f'attachment; filename={platform}_prompt.md'
    }

@app.route('/clear_session')
def clear_session():
    """Clear the session and start over."""
    session.clear()
    flash('Session cleared. You can start over now.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 