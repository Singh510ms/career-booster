"""
Parsers for extracting information from resumes and job postings.
"""

import os
import requests
from bs4 import BeautifulSoup
import PyPDF2
import tempfile
import re
import time
from urllib.parse import urlparse
import logging
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_resume_pdf(file_path):
    """
    Extract text from a resume PDF file.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                
            return text
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        return None

def fetch_job_posting(url):
    """
    Fetch and extract text from a job posting URL.
    
    Args:
        url (str): URL of the job posting
        
    Returns:
        str: Extracted text from the job posting
    """
    # In a real implementation, this would use requests to fetch the page
    return "Sample job posting text for demonstration purposes."

def parse_linkedin_job(url):
    """
    Parse job posting from LinkedIn.
    
    Args:
        url (str): LinkedIn job posting URL
        
    Returns:
        str: Extracted job description
    """
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # LinkedIn job descriptions are typically in a div with specific classes
        job_description = soup.find('div', {'class': 'description__text'})
        if not job_description:
            job_description = soup.find('div', {'class': 'show-more-less-html__markup'})
        
        if job_description:
            return clean_text(job_description.get_text())
        
        # If specific elements not found, try to find the main content
        main_content = soup.find('main')
        if main_content:
            return clean_text(main_content.get_text())
            
        return None
    except Exception as e:
        logger.error(f"Error parsing LinkedIn job: {e}")
        return None

def parse_indeed_job(url):
    """
    Parse job posting from Indeed.
    
    Args:
        url (str): Indeed job posting URL
        
    Returns:
        str: Extracted job description
    """
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Indeed job descriptions are typically in a div with specific ID or class
        job_description = soup.find('div', {'id': 'jobDescriptionText'})
        if not job_description:
            job_description = soup.find('div', {'class': 'jobsearch-jobDescriptionText'})
        
        if job_description:
            return clean_text(job_description.get_text())
            
        return None
    except Exception as e:
        logger.error(f"Error parsing Indeed job: {e}")
        return None

def parse_glassdoor_job(url):
    """
    Parse job posting from Glassdoor.
    
    Args:
        url (str): Glassdoor job posting URL
        
    Returns:
        str: Extracted job description
    """
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Glassdoor job descriptions are typically in a div with specific class
        job_description = soup.find('div', {'class': 'jobDescriptionContent'})
        if not job_description:
            job_description = soup.find('div', {'class': 'desc'})
        
        if job_description:
            return clean_text(job_description.get_text())
            
        return None
    except Exception as e:
        logger.error(f"Error parsing Glassdoor job: {e}")
        return None

def parse_generic_job(url):
    """
    Generic parser for job postings.
    
    Args:
        url (str): Job posting URL
        
    Returns:
        str: Extracted job description
    """
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Remove script, style, and nav elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.extract()
        
        # Look for common job description containers
        job_description = None
        
        # Try to find elements with job-related classes or IDs
        for class_name in ['job-description', 'description', 'jobDescription', 'job_description', 'job-details']:
            job_description = soup.find(['div', 'section', 'article'], {'class': re.compile(class_name, re.I)})
            if job_description:
                break
                
        for id_name in ['job-description', 'description', 'jobDescription', 'job_description', 'job-details']:
            job_description = soup.find(['div', 'section', 'article'], {'id': re.compile(id_name, re.I)})
            if job_description:
                break
        
        # If we found a job description container, extract text from it
        if job_description:
            return clean_text(job_description.get_text())
        
        # If no specific job description container found, try to extract from main content
        main_content = soup.find('main')
        if main_content:
            return clean_text(main_content.get_text())
        
        # If all else fails, extract text from the entire body
        body = soup.find('body')
        if body:
            return clean_text(body.get_text())
            
        return None
    except Exception as e:
        logger.error(f"Error parsing generic job: {e}")
        return None

def parse_aggressive(url):
    """
    Aggressive parsing method as a last resort.
    
    Args:
        url (str): Job posting URL
        
    Returns:
        str: Extracted text
    """
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text
        text = soup.get_text(separator='\n')
        
        # Clean up text
        return clean_text(text)
    except Exception as e:
        logger.error(f"Error in aggressive parsing: {e}")
        return None

def get_headers():
    """
    Get request headers that mimic a real browser.
    
    Returns:
        dict: Headers for HTTP requests
    """
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

def clean_text(text):
    """
    Clean up extracted text.
    
    Args:
        text (str): Raw text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return None
        
    # Clean up text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text

def save_temp_pdf(file):
    """
    Save an uploaded PDF file to a temporary location.
    
    Args:
        file (werkzeug.FileStorage): Uploaded PDF file
        
    Returns:
        str: Path to the saved file
    """
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)
    return file_path 