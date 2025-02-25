from crewai import Agent, Task, Crew
from langchain.tools import tool
from langchain_openai import OpenAI
import os
import logging
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize logger
logger = logging.getLogger(__name__)

class CareerBoosterAgents:
    """
    Defines the agents for the Career Booster application.
    """
    
    def __init__(self):
        """Initialize the agents."""
        # Explicitly use the API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        self.llm = OpenAI(api_key=api_key)
        self.project_ideation_agent = self._create_project_ideation_agent()
        self.project_planner_agent = self._create_project_planner_agent()
    
    def _create_project_ideation_agent(self):
        """Create the Project Ideation Agent."""
        return Agent(
            role="Project Ideation Consultant",
            goal="Generate relevant, impressive project ideas based on job descriptions and candidate skills that will help candidates stand out to employers",
            backstory="""You are an expert career consultant with 15+ years of experience helping 
            job seekers create impressive portfolio projects. You have deep knowledge of what hiring managers 
            and recruiters look for in candidates across various tech fields. You understand current industry 
            trends, in-demand technologies, and what makes a portfolio project truly stand out.
            
            You've helped thousands of candidates land jobs by suggesting projects that perfectly showcase 
            their existing skills while demonstrating their ability to learn and apply new technologies. 
            You're known for your ability to identify the exact type of projects that will impress employers 
            in specific domains and roles.
            
            You have access to web search capabilities and can thoroughly analyze job postings from any platform.
            You're skilled at extracting key requirements, technologies, and soft skills from job descriptions,
            even when they're not explicitly stated. You can identify the underlying needs of the role and
            suggest projects that address those needs.""",
            verbose=True,
            llm=self.llm,
            tools=[self.web_search, self.analyze_job_posting]
        )
    
    def _create_project_planner_agent(self):
        """Create the Project Planner Agent."""
        return Agent(
            role="Technical Project Planner",
            goal="Create detailed, actionable roadmaps for implementing portfolio projects that are realistic, well-structured, and showcase key skills",
            backstory="""You are a seasoned technical project manager with 12+ years of experience in software development. 
            You specialize in breaking down complex projects into manageable steps with clear timelines and resource requirements.
            
            You have extensive experience in agile methodologies and have successfully led hundreds of development projects 
            from concept to completion. You understand the technical challenges that developers face and know how to create 
            realistic timelines that account for learning curves, debugging, and testing.
            
            You're particularly skilled at creating roadmaps for portfolio projects that showcase a candidate's skills 
            while remaining achievable within tight timeframes. You know exactly which components should be prioritized 
            to demonstrate technical proficiency and which can be simplified to meet deadlines.""",
            verbose=True,
            llm=self.llm
        )

    @tool
    def web_search(self, query):
        """
        Perform a web search to gather additional information.
        
        Args:
            query (str): The search query
            
        Returns:
            str: Search results
        """
        try:
            import requests
            
            # This is a placeholder for a real web search API
            # In a production environment, you would use a service like SerpAPI, Google Custom Search API, etc.
            # For now, we'll return a message indicating the search would be performed
            
            return f"Web search performed for: {query}. In a production environment, this would return actual search results from a search API."
        except Exception as e:
            logger.error(f"Error performing web search: {e}")
            return f"Error performing web search: {e}"
    
    @tool
    def analyze_job_posting(self, url):
        """
        Analyze a job posting URL to extract detailed information.
        
        Args:
            url (str): The job posting URL
            
        Returns:
            str: Detailed analysis of the job posting
        """
        try:
            from parsers import fetch_job_posting
            
            # Fetch the job posting content
            job_content = fetch_job_posting(url)
            
            if not job_content:
                return "Could not fetch job posting content. Please check the URL and try again."
            
            # Analyze the job content
            system_message = """You are an expert job analyst with deep knowledge of the tech industry.
            
            Analyze the provided job posting and extract the following information:
            
            1. Job Title
            2. Company
            3. Required Technical Skills (list all mentioned technologies, languages, frameworks, etc.)
            4. Preferred/Nice-to-have Technical Skills
            5. Required Soft Skills
            6. Experience Level Required
            7. Job Responsibilities
            8. Industry/Domain
            9. Company Culture/Values (if mentioned)
            10. Key Problems This Role Will Solve
            
            Format your response as a structured analysis that can be used to generate relevant project ideas.
            """
            
            prompt = f"""
            # Job Posting Content
            {job_content}
            
            Please analyze this job posting and extract the key information as specified.
            """
            
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_message),
                ("user", prompt)
            ])
            return self.llm.invoke(prompt_template)
        except Exception as e:
            logger.error(f"Error analyzing job posting: {e}")
            return f"Error analyzing job posting: {e}"

    @tool
    def generate_project_ideas(self, job_description, candidate_skills):
        """
        Generate project ideas based on job description and candidate skills.
        
        Args:
            job_description (str): The job description text
            candidate_skills (str): The candidate's skills and interests
            
        Returns:
            str: 2-3 project ideas with descriptions
        """
        system_message = """You are an expert career consultant specializing in helping job seekers create portfolio projects that impress employers.

Your task is to analyze the provided job description and candidate's skills, then generate 2-3 project ideas that:
1. Directly align with the key requirements in the job description
2. Showcase the candidate's existing skills and strengths
3. Can be realistically built in under 2 weeks
4. Will stand out from typical portfolio projects in this field
5. Demonstrate problem-solving abilities and technical proficiency

For each project idea, provide:

## Project 1: [Compelling Project Name]
- **Overview**: A concise one-paragraph description of what the project does and why it's valuable
- **Key Technologies**: Specific technologies, frameworks, and tools that should be used (prioritize those mentioned in the job description)
- **Core Features**: 3-5 specific features that should be implemented, with the most impressive/relevant ones first
- **Technical Challenges**: 2-3 technical challenges this project will solve that demonstrate relevant skills
- **Unique Selling Point**: Why this project will stand out compared to typical portfolio projects
- **Alignment with Job Requirements**: How this project specifically demonstrates the key skills requested in the job description
- **Learning Opportunity**: One new skill or technology the candidate could incorporate to show growth potential

Ensure each project idea:
- Is specific and concrete (not vague or generic)
- Has a clear purpose and target user
- Demonstrates multiple skills mentioned in the job description
- Is appropriately scoped for a 1-2 week development timeline
- Would be impressive when featured on a resume or discussed in an interview

Analyze the job description carefully to identify:
- Must-have technical skills
- Nice-to-have technical skills
- Soft skills and qualities they're seeking
- The types of problems the role is expected to solve

Then match these with the candidate's existing skills to create project ideas that showcase their perfect fit for the role.
"""
        
        prompt = f"""
        # Job Description
        {job_description}
        
        # Candidate's Skills and Background
        {candidate_skills}
        
        Based on the above information, generate 2-3 portfolio project ideas that would help this candidate showcase their relevant skills for this specific job. The projects should be impressive yet achievable within 1-2 weeks.
        """
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", prompt)
        ])
        return self.llm.invoke(prompt_template)
    
    @tool
    def create_project_roadmap(self, project_idea, timeframe="2 weeks"):
        """
        Create a detailed roadmap for implementing a project.
        
        Args:
            project_idea (str): The selected project idea
            timeframe (str): The desired timeframe for completion (default: "2 weeks")
            
        Returns:
            str: A day-by-day or milestone-based roadmap
        """
        system_message = """You are a Technical Project Planner with extensive experience in software development and project management.

Your task is to create a detailed, day-by-day implementation roadmap for the given project idea that:
1. Breaks down the project into logical phases and specific tasks
2. Provides realistic time estimates for each task
3. Prioritizes features in the correct development order
4. Identifies potential technical challenges and how to address them
5. Suggests specific tools, libraries, and resources for each phase

Format your roadmap as follows:

# Project Roadmap: [Project Name]

## Phase 1: Project Setup and Foundation (Days 1-2)
- **Day 1: Environment Setup & Project Initialization**
  - Task 1: [Specific task description]
    - Tools/Technologies: [Specific tools, packages, or technologies needed]
    - Time estimate: [Hours]
    - Expected outcome: [What should be completed]
  - Task 2: [Specific task description]
    - Tools/Technologies: [Specific tools, packages, or technologies needed]
    - Time estimate: [Hours]
    - Expected outcome: [What should be completed]

## Phase 2: Core Functionality Development (Days 3-7)
[Follow the same format as above]

## Phase 3: UI/UX Implementation (Days 8-10)
[Follow the same format as above]

## Phase 4: Testing, Refinement, and Documentation (Days 11-14)
[Follow the same format as above]

## Technical Challenges and Solutions
- **Challenge 1**: [Describe a specific technical challenge]
  - **Solution**: [Provide a specific approach to solve it]
- **Challenge 2**: [Describe a specific technical challenge]
  - **Solution**: [Provide a specific approach to solve it]

## Resources and References
- [Provide specific documentation links, tutorials, or resources that will help]
- [Include GitHub repositories or code examples that could be helpful]

Ensure your roadmap:
- Is realistic for the given timeframe
- Accounts for learning curve if new technologies are involved
- Prioritizes MVP features first
- Includes time for testing and debugging
- Provides specific guidance rather than vague suggestions
- Breaks complex tasks into smaller, manageable steps
- Includes specific technical implementation details where helpful
- Suggests specific libraries, packages, or tools for each component
"""
        
        prompt = f"""
        # Project Idea
        {project_idea}
        
        # Timeframe
        {timeframe}
        
        Please create a detailed, day-by-day roadmap for implementing this project within the given timeframe. Include specific tasks, time estimates, tools/technologies needed, and expected outcomes for each day or phase.
        """
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", prompt)
        ])
        return self.llm.invoke(prompt_template)
    
    def create_crew(self):
        """
        Create a CrewAI crew with the defined agents and tasks.
        
        Returns:
            Crew: A CrewAI crew object
        """
        # Initialize agents if they don't exist (assuming these are defined elsewhere in the class)
        if not hasattr(self, 'project_ideation_agent'):
            # Initialize the agents
            self.initialize_agents()
        
        # Define tasks for the agents
        job_analysis_task = Task(
            description="Analyze the job description to identify key skills and requirements",
            expected_output="A detailed analysis of the job requirements and skills needed.",
            agent=self.project_ideation_agent,  # Use existing agent
            context=[],
        )
        
        resume_analysis_task = Task(
            description="Analyze the candidate's resume to identify their skills and experience",
            expected_output="A summary of the candidate's skills and experience.",
            agent=self.project_ideation_agent,  # Use existing agent
            context=[],
        )
        
        ideation_task = Task(
            description="Generate project ideas based on the job analysis and resume analysis",
            expected_output="A list of project ideas tailored to the candidate's skills and the job requirements.",
            agent=self.project_ideation_agent,
            context=[],
        )
        
        planning_task = Task(
            description="Create a detailed roadmap for implementing one of the project ideas",
            expected_output="A step-by-step roadmap for implementing one of the project ideas.",
            agent=self.project_planner_agent,
            context=[],
        )
        
        # Create the crew
        crew = Crew(
            agents=[self.project_ideation_agent, self.project_planner_agent],
            tasks=[job_analysis_task, resume_analysis_task, ideation_task, planning_task],
            verbose=True,
        )
        
        return crew