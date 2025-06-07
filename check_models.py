import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("🔴 API key (GOOGLE_API_KEY) not found. Check your .env file.")
else:
    try:
        genai.configure(api_key=api_key)
        print("✅ Successfully configured API key.")
        print("---")
        print("🤖 Available Models for Your Key:")
        
        # List all models that support generateContent
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")

    except Exception as e:
        print(f"🔴 An error occurred: {e}")