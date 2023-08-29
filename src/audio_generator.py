import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def create_audio_from_phrases(phrases):
  # API keys
  eleven_labs_key = os.environ.get('ELEVEN_LABS_API_KEY')

  print("Creating audios")

  for phrase in phrases:
    print(phrase)