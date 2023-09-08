from .state import StateHandler
import os
import requests
from dotenv import load_dotenv

def robot():
  # Initialize state handler and load content
  handler = StateHandler()
  content = handler.load()
  directory = 'audio'

  # Load the .env file
  load_dotenv()

  print("Creating audios...")

  # Ensure the directory exists
  if not os.path.exists(directory):
      os.makedirs(directory)

  url = "https://api.elevenlabs.io/v1/text-to-speech/5Z7y3RcIvAGUdlLFOUgk"

  headers = {
    "Accept": "audio/wav",
    "Content-Type": "application/json",
    "xi-api-key": os.environ.get('ELEVEN_LABS_API_KEY')
  }

  data = {
    "text": "",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.1,
      "similarity_boost": 0.5,
      "style": 1,
      "use_speaker_boost": False
    }
  }