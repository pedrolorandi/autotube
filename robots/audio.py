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

  print("Generating audios...")

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

  for idx, sentence in enumerate(content['sentences']):
    print(f"Creating audio #{idx}")

    text = sentence['text']
    data["text"] = text

    try:
      response = requests.post(url, json = data, headers = headers)
      response.raise_for_status()

      file_path = os.path.join(directory, f"audio_{idx}.wav")

      with open(file_path, "wb") as file:
        file.write(response.content)

    except requests.RequestException as e:
      print(f"Error for phrase {idx}: {e}")

  print("Audio generation complete.\n---")