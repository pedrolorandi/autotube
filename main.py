from pygooglenews import GoogleNews
import newspaper
import requests
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# API keys
openai_api_key = os.environ.get('OPENAI_API_KEY')

gn = GoogleNews()
search = gn.search('twitter', when = "24h")
entries = search['entries']

for entry in entries[:10]:
  print("Title:", entry['title'])
  link = entry['links'][0]['href']
  response = requests.get(link)

  # if response.status_code == 200:
  #   article = newspaper.Article(link)
  #   article.download()
  #   article.parse()
  #   text = article.text
  #   print(text)
  # else:
  #   print(f"Failed to retrieve the page for {entry['title']}")
  print("-----------------------------------------------")
  