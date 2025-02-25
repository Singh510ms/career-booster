#!/usr/bin/env python3
"""
Career Booster - A Multi-Agent System for generating portfolio project ideas
and roadmaps based on job descriptions and candidate skills.
"""

import os
import sys
import time
from agents import CareerBoosterAgents
from parsers import parse_resume_pdf, fetch_job_posting, save_temp_pdf
from prompt_generator import (
    generate_v0_prompt,
    generate_lovable_prompt,
    generate_replit_prompt,
    generate_generic_prompt
)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    clear_screen()
    print("=" * 80)
    print("                           CAREER BOOSTER                               ")
    print("=" * 80)
    print("Generate portfolio project ideas tailored to specific job descriptions")
    print("-" * 80)
    print()

def select_from_list(options, prompt="Select an option:"):
    """Let the user select an option from a list."""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")

def get_resume_path():
    """Get the path to the resume PDF file."""
    while True:
        resume_path = input("Enter the path to your resume PDF file: ")
        if os.path.exists(resume_path) and resume_path.lower().endswith('.pdf'):
            return resume_path
        else:
            print("Invalid file path or not a PDF file. Please try again.")

def get_job_url():
    """Get the job posting URL."""
    while True:
        job_url = input("Enter the URL of the job posting: ")
        if job_url.startswith(('http://', 'https://')):
            return job_url
        else:
            print("Invalid URL. Please enter a valid URL starting with http:// or https://")

def save_prompt_to_file(prompt, filename):
    """Save a prompt to a file."""
    os.makedirs('output', exist_ok=True)
    file_path = os.path.join('output', filename)
    
    with open(file_path, 'w') as f:
        f.write(prompt)
    
    return file_path

def main():
    """Main application function."""
    print_header()
    
    # Initialize agents
    try:
        career_booster = CareerBoosterAgents()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set up your .env file with the required API keys.")
        sys.exit(1)
    
    # Get resume PDF path
    resume_path = get_resume_path()
    
    # Parse resume
    print("\nParsing your resume...")
    resume_text = parse_resume_pdf(resume_path)
    if not resume_text:
        print("Failed to parse resume. Please check the file and try again.")
        sys.exit(1)
    
    # Get job posting URL
    job_url = get_job_url()
    
    # Fetch job posting
    print("\nFetching job posting...")
    job_description = fetch_job_posting(job_url)
    if not job_description:
        print("Failed to fetch job posting. Please check the URL and try again.")
        sys.exit(1)
    
    # Extract candidate skills from resume
    print("\nExtracting skills from your resume...")
    candidate_skills = resume_text  # For simplicity, we'll use the entire resume text
    
    # Generate project ideas
    print("\nGenerating project ideas based on your resume and the job posting...")
    try:
        project_ideas = career_booster.generate_project_ideas(job_description, candidate_skills)
        
        # Display project ideas
        clear_screen()
        print("=" * 80)
        print("                        PROJECT IDEAS                               ")
        print("=" * 80)
        print(project_ideas)
        print("\n")
        
        # Ask if the user wants to create a roadmap
        create_roadmap = input("Would you like to create a roadmap for one of these projects? (y/n): ").lower()
        
        if create_roadmap == 'y':
            # For simplicity, we'll ask the user to copy and paste the project idea they want
            print("\nPlease copy and paste the entire project idea you want to create a roadmap for:")
            selected_project = input("Project idea: ")
            
            # Ask for timeframe
            timeframe_options = ["1 week", "2 weeks", "3 weeks", "1 month"]
            timeframe_choice = select_from_list(timeframe_options, "Select a timeframe for your project:")
            timeframe = timeframe_options[timeframe_choice - 1]
            
            # Generate roadmap
            print(f"\nGenerating roadmap for a {timeframe} project...")
            roadmap = career_booster.create_project_roadmap(selected_project, timeframe)
            
            # Display roadmap
            clear_screen()
            print("=" * 80)
            print("                        PROJECT ROADMAP                            ")
            print("=" * 80)
            print(roadmap)
            print("\n")
            
            # Ask if the user wants to generate prompts for different platforms
            generate_prompts = input("Would you like to generate prompts for different platforms? (y/n): ").lower()
            
            if generate_prompts == 'y':
                # Generate prompts
                print("\nGenerating prompts for different platforms...")
                
                v0_prompt = generate_v0_prompt(selected_project, roadmap)
                lovable_prompt = generate_lovable_prompt(selected_project, roadmap)
                replit_prompt = generate_replit_prompt(selected_project, roadmap)
                generic_prompt = generate_generic_prompt(selected_project, roadmap)
                
                # Save prompts to files
                v0_file = save_prompt_to_file(v0_prompt, "v0_prompt.md")
                lovable_file = save_prompt_to_file(lovable_prompt, "lovable_prompt.md")
                replit_file = save_prompt_to_file(replit_prompt, "replit_prompt.md")
                generic_file = save_prompt_to_file(generic_prompt, "generic_prompt.md")
                
                # Display success message
                clear_screen()
                print("=" * 80)
                print("                        PROMPTS GENERATED                        ")
                print("=" * 80)
                print(f"Prompts have been saved to the following files:")
                print(f"- v0.dev: {v0_file}")
                print(f"- Lovable: {lovable_file}")
                print(f"- Replit: {replit_file}")
                print(f"- Generic: {generic_file}")
                print("\nYou can use these prompts on their respective platforms to create your project.")
            
    except Exception as e:
        print(f"Error: {e}")
        print("There was an error generating content. Please try again.")
    
    print("\nThank you for using Career Booster!")

if __name__ == "__main__":
    main() 