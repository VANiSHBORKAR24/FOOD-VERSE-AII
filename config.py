"""
Configuration and Environment Setup for Food-Verse AI
Supports both Google Gemini API Studio and Google Cloud Vertex AI
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the project directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Default Model configurations
DEFAULT_MODEL = "gemini-1.5-flash"
PRO_MODEL = "gemini-1.5-pro"

# Dietary options for the Multimodal Agent
DIETARY_PREFERENCES = [
    "None (Standard)",
    "Vegetarian",
    "Vegan",
    "Keto / Low-Carb",
    "High-Protein / Fitness",
    "Diabetic-Friendly",
    "Gluten-Free",
    "Halal",
    "Dairy-Free"
]

ALLERGEN_LIST = [
    "Peanuts",
    "Tree Nuts",
    "Dairy / Lactose",
    "Gluten / Wheat",
    "Eggs",
    "Soy",
    "Shellfish",
    "Fish",
    "Sesame"
]

CUISINE_OPTIONS = [
    "Any / Fusion",
    "Italian",
    "Indian",
    "Mexican",
    "East Asian (Chinese/Japanese/Thai)",
    "Mediterranean",
    "American",
    "Middle Eastern"
]


def get_api_key(override_key: str = None) -> str:
    """Retrieve API key from argument, environment, or return empty string."""
    if override_key and override_key.strip():
        return override_key.strip()
    return os.getenv("GEMINI_API_KEY", "").strip()
