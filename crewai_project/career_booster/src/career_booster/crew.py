from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.task import TaskOutput
import yaml
import os
import requests
import PyPDF2

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CareerBooster():
	"""CareerBooster crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@crew
	def crew(self) -> Crew:
		"""Creates the CareerBooster crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

class CareerBoosterCrew:
	def __init__(self, resume_path=None, job_url=None):
		"""Initialize the CareerBooster crew with optional resume path and job URL."""
		self.resume_path = resume_path
		self.job_url = job_url
		self.agents = self._load_agents()
		self.tasks = self._load_tasks()

	def _load_agents(self):
		"""Load agent configurations from YAML file."""
		with open(os.path.join(os.path.dirname(__file__), "config/agents.yaml"), "r") as file:
			agents_config = yaml.safe_load(file)

		agents = {}
		for name, config in agents_config.items():
			agents[name] = Agent(
				role=config['role'],
				goal=config['goal'],
				backstory=config['backstory'],
				llm=config.get('llm', 'cerebras/llama3.1-8b'),
			)
		return agents

	def _load_tasks(self):
		"""Load task configurations from YAML file."""
		with open(os.path.join(os.path.dirname(__file__), "config/tasks.yaml"), "r") as file:
			tasks_config = yaml.safe_load(file)

		tasks = {}
		for name, config in tasks_config.items():
			agent = self.agents.get(config['agent'])
			if not agent:
				continue
				
			# Create the enhanced description with context and inputs
			description = self._create_task_description(config)
			
			tasks[name] = Task(
				description=description,
				agent=agent,
				expected_output=config['expected_output'],
			)
		return tasks

	def _create_task_description(self, config):
		"""Create a task description with context and inputs."""
		# Start with the base description
		description = config['description']
		
		# Add context if available
		if 'context' in config and config['context']:
			description += f"\n\n### Context ###\n{config['context']}"
		
		# Add input data
		description += "\n\n### Input Data ###"
		
		# Add resume content if available
		if self.resume_path and os.path.exists(self.resume_path):
			# Check if it's a PDF file
			if self.resume_path.lower().endswith('.pdf'):
				try:
					resume_content = ""
					with open(self.resume_path, 'rb') as file:
						pdf_reader = PyPDF2.PdfReader(file)
						for page_num in range(len(pdf_reader.pages)):
							page = pdf_reader.pages[page_num]
							resume_content += page.extract_text()
				except Exception as e:
					resume_content = f"Error reading PDF: {str(e)}"
			else:
				# For text files
				try:
					with open(self.resume_path, 'r', encoding='utf-8') as file:
						resume_content = file.read()
				except UnicodeDecodeError:
					# Try with a different encoding if utf-8 fails
					with open(self.resume_path, 'r', encoding='latin-1') as file:
						resume_content = file.read()
					
			description += f"\n\n## Resume ##\n{resume_content}"
		
		# Add job information
		if self.job_url:
			if os.path.exists(self.job_url):
				# If it's a file path, read the file
				try:
					with open(self.job_url, 'r', encoding='utf-8') as file:
						job_content = file.read()
				except UnicodeDecodeError:
					# Try with a different encoding if utf-8 fails
					with open(self.job_url, 'r', encoding='latin-1') as file:
						job_content = file.read()
				description += f"\n\n## Job Description ##\n{job_content}"
			else:
				# Otherwise treat it as a URL
				try:
					response = requests.get(self.job_url)
					response.raise_for_status()  # Raise an exception for 4XX/5XX responses
					job_content = f"Job URL: {self.job_url}\n\nContent too large to include directly. Please visit the URL for details."
					description += f"\n\n## Job URL ##\n{job_content}"
				except Exception as e:
					description += f"\n\n## Job URL ##\n{self.job_url}\n\nError fetching job content: {str(e)}"
		
		return description

	def run(self):
		"""Run the crew tasks and return the results."""
		# Create a sequential process to ensure tasks run in the correct order
		crew = Crew(
			agents=list(self.agents.values()),
			tasks=[
				self.tasks.get('ideate_projects_task'),
				self.tasks.get('create_implementation_plan_task')
			],
			process=Process.sequential,
			verbose=True,
		)
		
		# Kick off the crew
		result = crew.kickoff()
		
		# Parse the results
		results_dict = {
			"project_ideas": None,
			"platform_prompts": None
		}
		
		# In CrewAI, the result may come in different formats
		# Try to parse the output from individual tasks
		try:
			# Check if we have task outputs in the result
			task_outputs = getattr(result, "task_outputs", None)
			
			if task_outputs and isinstance(task_outputs, list):
				# Extract outputs from each task
				for task_output in task_outputs:
					if isinstance(task_output, TaskOutput):
						task_description = task_output.task.description.lower()
						output = task_output.raw_output
						
						if "project ideas" in task_description or "ideate_projects_task" in str(task_output.task):
							results_dict["project_ideas"] = output
						elif "platform-specific prompt" in task_description or "create_implementation_plan_task" in str(task_output.task):
							results_dict["platform_prompts"] = output
			else:
				# If we can't access task outputs, use the raw result
				if isinstance(result, dict):
					return result
				else:
					# Default to using the string representation as both outputs
					results_dict["project_ideas"] = str(result)
					results_dict["platform_prompts"] = str(result)
		except Exception as e:
			# If we encounter any errors in parsing, fall back to the raw result
			print(f"Error parsing results: {str(e)}")
			if isinstance(result, dict):
				return result
			else:
				results_dict["project_ideas"] = str(result)
				results_dict["platform_prompts"] = str(result)
		
		return results_dict

	@agent
	def project_ideation_agent(self) -> Agent:
		"""Project Ideation Consultant who creates innovative project ideas."""
		return Agent(
			config=self.agents_config['project_ideation_agent'],
			verbose=True
		)

	@agent
	def project_planner_agent(self) -> Agent:
		"""Platform-Specific Prompt Engineer who creates prompts for Lovable, Bolt, and Replit."""
		return Agent(
			config=self.agents_config['project_planner_agent'],
			verbose=True
		)
