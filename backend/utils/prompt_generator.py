"""
Generate prompts for different platforms based on project ideas and roadmaps.
"""

def generate_v0_prompt(project_ideas, roadmap):
    """Generate a V0 prompt for the project."""
    return f"# Project Ideas\n\n{project_ideas}\n\n# Roadmap\n\n{roadmap}"

def generate_lovable_prompt(project_ideas, roadmap):
    """Generate a Lovable prompt for the project."""
    return f"# Lovable Project Ideas\n\n{project_ideas}\n\n# Roadmap\n\n{roadmap}"

def generate_replit_prompt(project_ideas, roadmap):
    """Generate a Replit prompt for the project."""
    return f"# Replit Project Ideas\n\n{project_ideas}\n\n# Roadmap\n\n{roadmap}"

def generate_generic_prompt(project_ideas, roadmap):
    """Generate a generic prompt for the project."""
    return f"# Generic Project Ideas\n\n{project_ideas}\n\n# Roadmap\n\n{roadmap}" 