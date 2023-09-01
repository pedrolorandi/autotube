# from src import create_content_from_articles, create_script_from_content, create_audio_from_phrases

# MAX_VALID_ARTICLES = 5

# content = create_content_from_articles('twitter', MAX_VALID_ARTICLES)
# phrases = create_script_from_content(content)
# audios = create_audio_from_phrases(phrases)

from robots import text_robot

robots = {
  'text': text_robot
}

def start():
  content = {}
  content['searchTerm'] = "Elon Musk"

  robots['text'](content)
  print(content)

if __name__ == "__main__":
  print("Process started")
  start()