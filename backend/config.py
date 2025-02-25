import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Cerebras API configuration
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CEREBRAS_API_URL = "https://inference.cerebras.ai/v1/completions"

# Model configuration
MODEL_NAME = "cerebras/Cerebras-GPT-4o-8k"  # Using Cerebras-GPT-4o model
MAX_TOKENS = 2048
TEMPERATURE = 0.7

# Validate configuration
if not CEREBRAS_API_KEY:
    print("Warning: CEREBRAS_API_KEY not found in environment variables.")
    print("Please set it in your .env file or environment.") 