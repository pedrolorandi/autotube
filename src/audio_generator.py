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

  file_counter = 1

  for phrase in phrases:

    # Skip if the phrase is empty
    if not phrase.strip():
      continue

    print(f"Creating audio #{file_counter}")
    print(phrase)

    data["text"] = phrase

    try:
      response = requests.post(url, json = data, headers = headers)
      response.raise_for_status()

      file_path = os.path.join(directory, f"audio_{file_counter}.wav")

      with open(file_path, "wb") as file:
        file.write(response.content)

      file_counter += 1

    except requests.RequestException as e:
      print(f"Error for phrase {file_counter}: {e}")

  print("-----------------------------------------------")