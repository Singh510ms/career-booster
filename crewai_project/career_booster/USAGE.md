# Career Booster - Usage Guide

This guide provides detailed instructions on how to use the Career Booster tool to generate project ideas and platform-specific prompts for your job applications.

## Overview

The Career Booster is a CrewAI-powered tool that:
1. Analyzes your resume and a job description
2. Generates 2-3 tailored project ideas that you can build in under 2 weeks
3. Creates ready-to-use prompts for Lovable.dev, Bolt.new, and Replit

This helps you stand out as a candidate by quickly creating relevant portfolio projects using AI-assisted development platforms.

## Prerequisites

Before using the Career Booster, ensure you have:

1. Python 3.9+ installed
2. Cerebras API key (set in your `.env` file)
3. Required packages installed (instructions below)
4. Access to at least one of these platforms:
   - [Lovable.dev](https://www.lovable.dev/) - For UI/UX design
   - [Bolt.new](https://Bolt.new/) - For web/blockchain components
   - [Replit](https://replit.com/) - For code implementation

## Installation

```bash
# Clone the repository (if you haven't already)
git clone <repository-url>
cd career_booster

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .

# Install additional dependencies for PDF processing
pip install PyPDF2 requests
```

## Setting Up Your Environment

Create a `.env` file in the root directory with your API key:

```
CEREBRAS_API_KEY=your_api_key_here
```

## Running Career Booster

### Option 1: Using the Test Script (Simplest)

The test script provides a straightforward way to run the Career Booster:

```bash
# Navigate to the career_booster directory
cd crewai_project/career_booster

# Run with both resume and job URL, saving output to a file
python test_career_booster.py /path/to/your/resume.pdf "https://company.com/job-posting" results.md

# Or without saving to a file
python test_career_booster.py /path/to/your/resume.pdf "https://company.com/job-posting"
```

### Option 2: Using the CLI Tool

The CLI tool provides more options:

```bash
# Navigate to the career_booster directory
cd crewai_project/career_booster

# Run with both resume and job URL, saving output to a file
python -m career_booster.main --resume /path/to/your/resume.pdf --job "https://company.com/job-posting" --output results.md

# Or with just a resume
python -m career_booster.main --resume /path/to/your/resume.pdf
```

## Input Files

The Career Booster works best with the following inputs:

### Resume File

Your resume can be in PDF or text format. The system will extract text from PDFs automatically.

### Job Description

You can provide a job description in two ways:
1. As a URL to the job posting (recommended)
2. As a text file containing the job description

## Output and How to Use It

The Career Booster generates two main outputs:

### 1. Project Ideas

2-3 project ideas tailored to the job description and your skills. Each idea includes:
- A project overview (one-liner)
- Key tech tools and skills
- The unique selling point

### 2. Platform-Specific Prompts

For each project idea, you'll receive prompts for three different platforms:

#### Lovable.dev Prompts
Copy and paste these prompts into [Lovable.dev](https://www.lovable.dev/) to generate UI designs, mockups, and user flows for your project. These prompts will help you create professional-looking interfaces with minimal design experience.

#### Bolt.new Prompts
Use these prompts in [Bolt.New](https://bolt.new/) to generate web components or blockchain elements (if applicable). These prompts are designed to create functional web components that can be integrated into your project.

#### Replit Prompts
Paste these prompts into [Replit](https://replit.com/) to generate the core functionality and code implementation for your project. These prompts will help you quickly create working code that you can further customize.

## Step-by-Step Usage

1. **Generate ideas and prompts**:
   ```bash
   python test_career_booster.py /path/to/resume.pdf "https://job-url.com" results.md
   ```

2. **Review the generated project ideas** in the terminal or results file and select one that appeals to you.

3. **Use the Lovable.dev prompt** to generate the UI/UX for your selected project.

4. **Use the Bolt.new prompt** to create any web components or infrastructure needed.

5. **Use the Replit prompt** to implement the core functionality.

6. **Combine and refine** the outputs to create your complete portfolio project.

7. **Document your process** and add the project to your resume or portfolio.

## Example

```bash
python test_career_booster.py resume.pdf "https://company.com/job-posting" results.md
```

The results.md file will contain:
- Project ideas with overviews, tools, and unique selling points
- Ready-to-use prompts for Lovable.dev, Bolt.new, and Replit

## Troubleshooting

If you encounter issues:

1. Check your `.env` file to ensure your API key is correct
2. Make sure your resume file exists and is readable
3. Verify your job URL is accessible
4. Check that you have installed all required dependencies

## Customization

You can customize the agents and tasks by modifying:
- `src/career_booster/config/agents.yaml`: Configure the agent roles, goals, and backstories
- `src/career_booster/config/tasks.yaml`: Modify task descriptions and expected outputs 