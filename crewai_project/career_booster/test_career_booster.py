#!/usr/bin/env python

from dotenv import load_dotenv
import sys
import os

# Add the src directory to the path so we can import our module
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from career_booster.crew import CareerBoosterCrew

def main():
    """
    Test script for the Career Booster Crew.
    """
    load_dotenv()  # Load environment variables from .env file
    
    # Get resume path from command line or use default
    resume_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Get job URL from command line or use default
    job_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Get output file path from command line (optional)
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    print("⚡️ Starting Career Booster Test...")
    print(f"Resume path: {resume_path}")
    print(f"Job URL: {job_url}")
    
    # Create and run the crew
    career_crew = CareerBoosterCrew(
        resume_path=resume_path,
        job_url=job_url
    )
    
    print("🔍 Analyzing resume and job description...")
    
    results = career_crew.run()
    
    print("\n" + "="*50)
    print("🚀 RESULTS:")
    print("="*50)
    
    if isinstance(results, dict):
        if "project_ideas" in results:
            print("\n" + "="*50)
            print("🚀 PROJECT IDEAS:")
            print("="*50)
            print(results["project_ideas"])
        
        if "platform_prompts" in results:
            print("\n" + "="*50)
            print("💻 PLATFORM PROMPTS:")
            print("="*50)
            print(results["platform_prompts"])
            
        # Save to file if specified
        if output_file:
            with open(output_file, "w") as f:
                f.write("# Career Booster Results\n\n")
                f.write("## Project Ideas\n\n")
                f.write(results.get("project_ideas", "No project ideas generated."))
                f.write("\n\n## Platform Prompts\n\n")
                f.write(results.get("platform_prompts", "No platform prompts generated."))
            print(f"\n✅ Results saved to {output_file}")
    else:
        # If results is not a dictionary, print it directly
        print(results)
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 