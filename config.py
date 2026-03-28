"""
Configuration module for NaukriAgent.
Sets up the fine-tuned SLM and environment variables.
"""

import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- SLM CONFIGURATION ---
# Replace with your local Ollama, vLLM, or other SLM provider endpoint
SLM_MODEL_NAME = os.getenv("SLM_MODEL_NAME", "phi-3-fine-tuned-hr")
SLM_BASE_URL = os.getenv("SLM_BASE_URL", "http://localhost:11434/v1")
SLM_API_KEY = os.getenv("SLM_API_KEY", "ollama")

def get_slm():
    """
    Initialize and return the fine-tuned SLM (Small Language Model).
    
    Returns:
        ChatOpenAI: Configured language model instance.
    
    Raises:
        ConnectionError: If unable to connect to the SLM provider.
    """
    try:
        slm = ChatOpenAI(
            model=SLM_MODEL_NAME,
            base_url=SLM_BASE_URL,
            api_key=SLM_API_KEY,
            temperature=0.7,
            max_tokens=2000
        )
        return slm
    except Exception as e:
        raise ConnectionError(
            f"Failed to connect to SLM at {SLM_BASE_URL}. "
            f"Ensure your Ollama/vLLM server is running. Error: {e}"
        )

# --- APPLICATION CONFIGURATION ---
APPROVAL_REQUIRED = os.getenv("APPROVAL_REQUIRED", "true").lower() == "true"
DEFAULT_SCORE_THRESHOLD = int(os.getenv("DEFAULT_SCORE_THRESHOLD", "75"))
