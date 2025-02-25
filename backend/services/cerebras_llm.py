import requests
import json
from config import CEREBRAS_API_KEY, CEREBRAS_API_URL, MODEL_NAME, MAX_TOKENS, TEMPERATURE

class CerebrasLLM:
    """
    A class to handle interactions with the Cerebras LLM API.
    """
    
    def __init__(self):
        self.api_key = CEREBRAS_API_KEY
        self.api_url = CEREBRAS_API_URL
        self.model = MODEL_NAME
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        
        if not self.api_key:
            raise ValueError("Cerebras API key is required. Please set CEREBRAS_API_KEY in your .env file.")
    
    def generate_completion(self, prompt, system_message=None):
        """
        Generate a completion using the Cerebras LLM API.
        
        Args:
            prompt (str): The user prompt to send to the model
            system_message (str, optional): System message to guide the model's behavior
            
        Returns:
            str: The generated text response
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Prepare the payload
        payload = {
            "model": self.model,
            "messages": [],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        # Add system message if provided
        if system_message:
            payload["messages"].append({"role": "system", "content": system_message})
        
        # Add user prompt
        payload["messages"].append({"role": "user", "content": prompt})
        
        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            print(f"Error calling Cerebras API: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            return f"Error: Failed to get response from Cerebras API. {str(e)}" 