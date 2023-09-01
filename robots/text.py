from pygooglenews import GoogleNews
from dotenv import load_dotenv
import newspaper
import requests
import re
import os
import openai

def robot(content):
  def fetch_news(query, duration="24h"):
    print("Fetching news")

    gn = GoogleNews()
    search = gn.search(query, when=duration)
    entries = search['entries']
    
    content['entries'] = []

    for entry in entries:
      new_entry = {
          'title': entry['title'],
          'link': entry['link']
      }

      content['entries'].append(new_entry)

    print("News fetching complete.\n---")

  def parse_news(content):
    print("Parsing news")

    valid_articles_count = 0
    content['articles'] = []

    for entry in content['entries']:
      if valid_articles_count == 5:
        break
  
      print("Title:", entry['title'])

      try:
        response = requests.get(entry['link'], timeout=10)
        response.raise_for_status()
        
        article = newspaper.Article(entry['link'])
        article.set_html(response.content)
        article.parse()
    
        text = article.text
        text = re.sub(r'\n+', '', text)
        text = re.sub(r'\s*Advertisement\s*', '', text)
        
        new_article = {
          'title': entry['title'],
          'text': text
        }

        content['articles'].append(new_article)
        valid_articles_count += 1

        print("Article added")
    
      except requests.RequestException as e:
          print(f"Failed to fetch {entry['link']} due to error: {e}")
      except Exception as e:
          print(f"An error occurred while processing the article: {e}")

      print("---")

    print("News parsing complete.\n---")

  def generate_content(content):
    print("Generating content")

    full_content = ""

    for article in content['articles']:
      full_content += "Title: " + article['title'] + "."
      full_content += article['text'] + " | "

    content['content'] = full_content

    print("Content generation complete.\n---")

  def generate_script(content):
    # Load the .env file
    load_dotenv()

    # API keys
    openai.organization = os.environ.get('OPENAI_ORG_ID')
    openai.api_key = os.environ.get('OPENAI_API_KEY')

  fetch_news(content['searchTerm'])
  parse_news(content)
  generate_content(content)
  # generate_script(content)