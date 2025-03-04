#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv
import argparse
import os

from datetime import datetime

from .crew import CareerBoosterCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def main():
    """
    Main entry point for the Career Booster CLI.
    """
    load_dotenv()  # Load environment variables from .env file
    
    parser = argparse.ArgumentParser(description='Career Booster - Generate project ideas and platform-specific prompts based on resume and job description.')
    
    parser.add_argument('--resume', type=str, help='Path to the resume file (PDF, TXT, etc.)')
    parser.add_argument('--job', type=str, help='URL or path to job description')
    parser.add_argument('--output', type=str, help='Path to save output (default: output.md)')
    
    args = parser.parse_args()
    
    if not args.resume and not args.job:
        print("Please provide at least one of --resume or --job")
        parser.print_help()
        sys.exit(1)
    
    # Create and run the crew
    career_crew = CareerBoosterCrew(
        resume_path=args.resume,
        job_url=args.job
    )
    
    print("⚡️ Starting Career Booster...")
    print(f"Resume: {args.resume if args.resume else 'Not provided'}")
    print(f"Job: {args.job if args.job else 'Not provided'}")
    print("🔍 Analyzing resume and job description...")
    
    results = career_crew.run()
    
    # Check if results is a dictionary
    if isinstance(results, dict):
        project_ideas = results.get("project_ideas", "No project ideas generated.")
        platform_prompts = results.get("platform_prompts", "No platform prompts generated.")
        
        print("\n" + "="*50)
        print("🚀 PROJECT IDEAS:")
        print("="*50)
        print(project_ideas)
        
        print("\n" + "="*50)
        print("💻 PLATFORM PROMPTS:")
        print("="*50)
        print(platform_prompts)
        
        # Save output to file if requested
        if args.output:
            output_path = args.output
            if not output_path.endswith(".md"):
                output_path += ".md"
                
            with open(output_path, "w") as f:
                f.write("# Career Booster Results\n\n")
                f.write("## Project Ideas\n\n")
                f.write(project_ideas)
                f.write("\n\n## Platform Prompts\n\n")
                f.write(platform_prompts)
                
            print(f"\n✅ Results saved to {output_path}")
    else:
        # If results is not a dictionary, print it directly
        print("\n" + "="*50)
        print("🚀 RESULTS:")
        print("="*50)
        print(results)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

def run():
    """
    Run the crew with the CareerBooster class.
    This is used when invoking via the crewai CLI.
    """
    from datetime import datetime
    
    inputs = {
        'topic': 'Career Project Ideas',
        'current_year': str(datetime.now().year)
    }
    
    try:
        # Use the CrewBase class for CLI runs
        CareerBooster().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CareerBooster().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CareerBooster().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CareerBooster().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
