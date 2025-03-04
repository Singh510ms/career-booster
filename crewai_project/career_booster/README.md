# Career Booster

A CrewAI project that helps job seekers generate impressive portfolio project ideas and platform-specific prompts based on their resume and job descriptions.

## Features

- **Project Ideation**: Generate 2-3 project ideas tailored to showcase your skills for specific jobs, buildable within 2 weeks
- **Platform Prompts**: Get ready-to-use prompts for Lovable.dev, Bolt.new, and Replit to quickly generate impressive portfolio projects
- **Resume & Job Description Analysis**: Customized recommendations based on your skills and job requirements

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd career_booster

# Install the package in development mode
pip install -e .

# Install required packages for PDF processing
pip install PyPDF2 requests
```

## Prerequisites

1. Cerebras API key (set in your `.env` file)

## Configuration

The project uses YAML files to configure agents and tasks. You can customize:

- Agent roles, goals, and backstories in `src/career_booster/config/agents.yaml`
- Task descriptions and contexts in `src/career_booster/config/tasks.yaml`

## Key Agents

1. **Project Ideation Consultant**: Analyzes job descriptions and candidate skills to generate 2-3 innovative project ideas that can be built in under 2 weeks.

2. **Platform-Specific Prompt Engineer**: Creates detailed prompts for Lovable.dev, Bolt.New, and Replit that allow you to quickly generate impressive portfolio projects.

## Usage

### Using the Test Script

For quick testing, you can use the provided test script:

```bash
# Run with a resume file and job URL, optionally saving to a file
python test_career_booster.py path/to/resume.pdf "https://joburl.com/job-posting" [output_file.md]

# Or with just a resume file (specify a job later)
python test_career_booster.py path/to/resume.pdf
```

### Using the CLI

You can run the project directly using the CLI:

```bash
# Run with a resume file and job URL
python -m career_booster.main --resume path/to/resume.pdf --job "https://joburl.com/job-posting" --output results.md

# Or just with a resume
python -m career_booster.main --resume path/to/resume.pdf
```

## Using CrewAI CLI

This project is set up to work with the CrewAI CLI. You can run:

```bash
# Run the crew directly
crewai run

# Start interactive mode
crewai run -i
```

## Output

The program generates two main outputs:

1. **Project Ideas**: A list of 2-3 project ideas, each with a clear overview, key tech tools/skills, and unique selling point. The ideas are realistic to complete in 2 weeks and directly relevant to the job description.

2. **Platform Prompts**: Ready-to-use prompts for:
   - **Lovable.dev**: Design and UI/UX prompts for creating interfaces and mockups
   - **Bolt.New**: Prompts for web3/blockchain components or general web application elements
   - **Replit**: Code implementation prompts for the core functionality

Simply copy and paste these prompts into their respective platforms to quickly generate components of your portfolio project.

## Example Command

```bash
# Run with a specific resume and job posting URL, saving to results.md
python test_career_booster.py /path/to/your/resume.pdf "https://company.com/job-posting" results.md
```

## License

MIT
