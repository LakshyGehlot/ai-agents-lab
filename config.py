import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API KEYs
openAiKey = os.getenv("OPENAI_API_KEY")
geminiKey = os.getenv("GEMINI_API_KEY")
