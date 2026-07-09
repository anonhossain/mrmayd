#app/backend/src/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Dynamically locate the .env file relative to this file (backend/src/.env)
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class Config:
    def __init__(self):
        # Extract environment variables
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_VISION_MODEL = "gpt-4o"  # Adjusted placeholder string
        self.PDF_RENDER_DPI = 200

        # Basic settings for OpenAI API usage
        self.OPENAI_MODEL_BASIC = "gpt-4.1"
        self.TEMPERATURE_BASIC = 0.6
        self.MAXIMUM_TOKENS_BASIC = 1500

        # COVER LETTER GENERATION SETTINGS
        self.OPENAI_MODEL_COVER_LETTER = "gpt-4o"
        self.TEMPERATURE_COVER_LETTER = 0.6
        self.MAXIMUM_TOKENS_COVER_LETTER = 1500

        # INTERVIEW QUESTIONS GENERATION SETTINGS
        self.OPENAI_MODEL_INTERVIEW_QUESTIONS = "gpt-4o"
        self.TEMPERATURE_INTERVIEW_QUESTIONS = 0.7
        self.MAXIMUM_TOKENS_INTERVIEW_QUESTIONS = 2000

        # Suggestions
        self.OPENAI_MODEL_SUGGESTIONS = "gpt-4.1"
        self.TEMPERATURE_SUGGESTIONS = 0.4
        self.MAXIMUM_TOKENS_SUGGESTIONS = 500

        # INTERVIEW EVALUATION SETTINGS
        self.OPENAI_MODEL_INTERVIEW_EVALUATION = "gpt-5.1"
        self.TEMPERATURE_INTERVIEW_EVALUATION = 0.5
        self.MAXIMUM_TOKENS_INTERVIEW_EVALUATION = 2000
        self.PROMPT_CACHE_RETENTION = "24h"  # Retain prompt cache for 24 hours
        self.REASONING_EFFORT ={"effort": "low"}  # Maximum tokens for prompt cache

        # Speech-to-Text Model
        self.OPENAI_STT_MODEL= "whisper-1"

        # CV Improvement Settings
        self.OPENAI_MODEL_CV_IMPROVEMENT = "gpt-5.1"
        self.TEMPERATURE_CV_IMPROVEMENT = 0.5
        self.MAXIMUM_TOKENS_CV_IMPROVEMENT = 16000
        self.PROMPT_CACHE_RETENTION_CV_IMPROVEMENT = "24h"  # Retain prompt cache for 24 hours
        self.REASONING_EFFORT_CV_IMPROVEMENT ={"effort": "low"}

# Initialize the settings instance
settings = Config()