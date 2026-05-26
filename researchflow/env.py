"""Environment configuration helper for local and Streamlit Cloud deployment."""
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

def get_api_key(key_name: str) -> str:
    """Get API key from environment or Streamlit secrets."""
    # First try environment variable (local .env)
    value = os.getenv(key_name)
    if value:
        return value
    
    # Try Streamlit secrets (cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    
    raise ValueError(f"Missing API key: {key_name}")
