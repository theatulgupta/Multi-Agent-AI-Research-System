"""Environment configuration helper for local and Streamlit Cloud deployment."""
import os
import sys
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

def get_api_key(key_name: str) -> str:
    """Get API key from environment or Streamlit secrets.
    
    Args:
        key_name: Name of the API key to retrieve
        
    Returns:
        API key value
        
    Raises:
        ValueError: If API key is not found in environment or secrets
    """
    # First try environment variable (local .env)
    value = os.getenv(key_name)
    if value:
        return value
    
    # Try Streamlit secrets (cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key_name in st.secrets:
            return st.secrets[key_name]
    except ImportError:
        pass
    except Exception as e:
        print(f"Warning: Could not access Streamlit secrets: {e}", file=sys.stderr)
    
    raise ValueError(
        f"Missing API key: {key_name}. "
        f"Please set it in .env file or Streamlit secrets."
    )
