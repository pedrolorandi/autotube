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
    print("Generating script")

    # Load the .env file
    load_dotenv()

    # API keys
    openai.organization = os.environ.get('OPENAI_ORG_ID')
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    user_prompt = content['content'] + "With the information provided, write a youtube script using informal, opinionated, and somewhat satirical tone. Use casual language and often employ sarcasm to make points. Use a sense of skepticism towards media narratives and a desire to present a more down-to-earth perspective on events. The tone should be somewhat confrontational at times, challenging conventional ideas and encouraging the audience to think critically. Overall, the tone should be a blend of commentary, critique, and humor. To add pauses in the script, add a simple dash (-) or the em-dash (—). The script should contain 2000 words. Don't write introduction and conclusion paragraphs. Don't welcome back people to the channel, and don't use conclusive phrases like 'See you next time'. WRITE THE SPEAKING PART ONLY."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=1,
        messages=[
          {"role": "user", "content": user_prompt}
        ]
    )

    content['script'] = response.choices[0].message.content

    print("Script generation complete.\n---")

  fetch_news(content['searchTerm'])
  parse_news(content)
  generate_content(content)
  generate_script(content)