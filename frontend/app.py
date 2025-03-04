import os
import shutil
import re
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import sys

# Add the CrewAI backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'crewai_project/career_booster/src'))
from career_booster.crew import CareerBoosterCrew

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def parse_crew_output(crew_output):
    """
    Parse the raw output from CrewAI into structured data for the frontend.
    
    Args:
        crew_output: Dictionary with 'project_ideas' and 'platform_prompts' keys.
        
    Returns:
        Dictionary with structured data for the frontend.
    """
    results = {
        'project_ideas': [],
        'platform_prompts': {
            'lovable': '',
            'bolt': '',
            'replit': ''
        }
    }
    
    # Check if we have valid input
    if not isinstance(crew_output, dict):
        return results
    
    # Extract project ideas
    project_ideas_text = crew_output.get('project_ideas', '')
    if isinstance(project_ideas_text, str) and project_ideas_text.strip():
        # Split the text into projects
        projects = []
        
        # Try to extract projects using regex patterns
        project_pattern = r'(?:Project|Idea)\s*(?:\#?|\d+)?\s*:?\s*([^\n]+)(.*?)(?=(?:Project|Idea)\s*(?:\#?|\d+)?\s*:|\Z)'
        matches = list(re.finditer(project_pattern, project_ideas_text, re.DOTALL))
        
        if matches:
            for match in matches:
                title = match.group(1).strip()
                content = match.group(2).strip()
                
                # Extract description, tech stack, and unique value
                description = content
                tech_stack = ''
                unique_value = ''
                
                # Look for project overview or description
                overview_match = re.search(r'(?:Project Overview|Overview|Description):\s*(.*?)(?=(?:Key Tech|Technology|Tech Stack|Unique|$))', content, re.DOTALL)
                if overview_match:
                    description = overview_match.group(1).strip()
                
                # Look for tech tools/skills
                tech_match = re.search(r'(?:Key Tech Tools|Technology Stack|Tech Stack|Key Tech|Technologies):\s*(.*?)(?=(?:Unique|$))', content, re.DOTALL)
                if tech_match:
                    tech_stack = tech_match.group(1).strip()
                
                # Look for unique selling point
                usp_match = re.search(r'(?:Unique Selling Point|Unique Value|USP|Unique Feature|Value):\s*(.*?)(?=$)', content, re.DOTALL)
                if usp_match:
                    unique_value = usp_match.group(1).strip()
                
                projects.append({
                    'title': title,
                    'description': description,
                    'tech_stack': tech_stack,
                    'unique_value': unique_value
                })
        
        results['project_ideas'] = projects
    
    # Extract platform prompts
    platform_prompts_text = crew_output.get('platform_prompts', '')
    if isinstance(platform_prompts_text, str) and platform_prompts_text.strip():
        # Extract each platform's prompt using the new structured format
        sections = re.split(r'###\s*([^#]+?)\s*###', platform_prompts_text)
        
        # Process sections (skipping the first empty section if it exists)
        for i in range(1, len(sections), 2):
            section_name = sections[i].lower().strip()
            section_content = sections[i + 1].strip() if i + 1 < len(sections) else ''
            
            if 'lovable' in section_name:
                results['platform_prompts']['lovable'] = section_content
            elif 'bolt' in section_name:
                results['platform_prompts']['bolt'] = section_content
            elif 'replit' in section_name:
                results['platform_prompts']['replit'] = section_content
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Clear session data from previous runs
    if 'resume_path' in session:
        session.pop('resume_path')
    if 'job_url' in session:
        session.pop('job_url')
    
    # Check if a file was uploaded
    if 'resume' not in request.files:
        return render_template('index.html', error="No file uploaded")
    
    file = request.files['resume']
    if file.filename == '':
        return render_template('index.html', error="No file selected")
    
    job_url = request.form.get('job_url', '').strip()
    if not job_url:
        return render_template('index.html', error="Job URL is required")
    
    # Save the uploaded resume
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Store the file path and job URL in the session
    session['resume_path'] = file_path
    session['job_url'] = job_url
    
    # Redirect to the processing page
    return redirect(url_for('processing'))

@app.route('/processing')
def processing():
    if 'resume_path' not in session or 'job_url' not in session:
        return redirect(url_for('index'))
    
    return render_template('processing.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'resume_path' not in session or 'job_url' not in session:
        return jsonify({'error': 'Missing resume or job URL'}), 400
    
    try:
        # Get data from session
        resume_path = session.get('resume_path')
        job_url = session.get('job_url')
        
        # Initialize the CrewAI backend
        crew = CareerBoosterCrew(resume_path=resume_path, job_url=job_url)
        
        # Run the backend and get results
        raw_results = crew.run()
        
        # Parse the raw results into structured data
        parsed_results = parse_crew_output(raw_results)
        
        # Store parsed results in session
        session['results'] = parsed_results
        
        return jsonify({'status': 'success'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results')
def results():
    if 'results' not in session:
        return redirect(url_for('index'))
    
    return render_template('results.html', results=session['results'])

@app.route('/clear', methods=['POST'])
def clear():
    # Clear session data
    session.clear()
    
    # Clear uploads folder
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)