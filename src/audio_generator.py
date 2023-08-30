import os
import requests
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def create_audio_from_phrases(phrases, directory = "audio"):
  print("Creating audios")

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

  for i, phrase in enumerate(phrases, start = 1):
    print(f"Creating audio #{i}")

    data["text"] = phrase

    try:
      response = requests.post(url, json = data, headers = headers)
      response.raise_for_status()

      file_path = os.path.join(directory, f"audio_{i}.wav")

      with open(file_path, "wb") as file:
        file.write(response.content)

    except requests.RequestException as e:
      print(f"Error for phrase {i}: {e}")

  print("-----------------------------------------------")