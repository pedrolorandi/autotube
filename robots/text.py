from pygooglenews import GoogleNews
from dotenv import load_dotenv
from .state import StateHandler
from newspaper import Article
import requests
import re
import os
import openai

def robot():
  # Initialize state handler and load content
  handler = StateHandler()
  content = handler.load()  

  def fetch_news(query, duration="24h"):
    """Fetches news articles based on the query and duration provided.
    
    Parameters:
    - query (str): The search query for fetching news articles.
    - duration (str): The time duration for which to fetch news articles.

    Returns:
    - None
    """
    print("Fetching news...")

    try:
      gn = GoogleNews()
      search = gn.search(query, when=duration)
      entries = search['entries']

      content['entries'] = [
        {'title': entry['title'], 'link': entry['link']}
        for entry in entries[:10]
      ]
    except Exception as e:
      print(f"An error occurred while fetching the news: {e}")
    else:
      print("News fetching complete.\n---")

  def parse_news(content):
    """Parses the news articles from the links stored in the content dictionary.
    
    Parameters:
    - content (dict): The content dictionary storing the news data.

    Returns:
    - None
    """
    print("Parsing news...")

    newline_regex = re.compile(r'\n+')
    adv_regex = re.compile(r'\s*Advertisement\s*')

    valid_articles_count = 0
    content['articles'] = []

    for entry in content.get('entries', []):
      if valid_articles_count >= 5:
        break

      print("Title:", entry['title'])

      try:
        response = requests.get(entry['link'], timeout = 10)
        response.raise_for_status()

        # Extract and clean the article text
        article = Article(entry['link'])
        article.set_html(response.content)
        article.parse()

        text = article.text
        text = newline_regex.sub('', text)
        text = adv_regex.sub('', text)

        content['articles'].append({'title': entry['title'], 'text': text})
        valid_articles_count += 1
        print("Article added")
      except requests.RequestException as e:
        print(f"Failed to fetch {entry['link']} due to error: {e}")
      except Exception as e:
        print(f"An error occurred while processing the article: {e}")

      print("---")
    
    print("News parsing complete.\n---")

  def generate_content(content):
    # Generate concatenated content from parsed articles
    print("Generating content...")
    full_content = ""

    for article in content['articles']:
      full_content += "Title: " + article['title'] + "."
      full_content += article['text'] + " | "

    content['content'] = full_content
    print("Content generation complete.\n---")

  def generate_script(content):
    # Generate a script using OpenAI's GPT-4
    print("Generating script, please wait...")
    load_dotenv()

    openai.organization = os.environ.get('OPENAI_ORG_ID')
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    user_prompt = content['content'] + "With the information provided, write a youtube script using informal, opinionated, and somewhat satirical tone. Use casual language and often employ sarcasm to make points. Use a sense of skepticism towards media narratives and a desire to present a more down-to-earth perspective on events. The tone should be somewhat confrontational at times, challenging conventional ideas and encouraging the audience to think critically. Overall, the tone should be a blend of commentary, critique, and humor. To add pauses in the script, add a simple dash (-) or the em-dash (—). The script should contain 3000 words. Don't write introduction and conclusion paragraphs. Don't welcome back people to the channel, and don't use conclusive phrases like 'See you next time'. WRITE THE SPEAKING PART ONLY."
    
    response = openai.ChatCompletion.create(
      model="gpt-4",
      temperature=1,
      messages=[
          {"role": "user", "content": user_prompt}
      ]
    )

    content['script'] = response.choices[0].message.content
    print("Script generation complete.\n---")

  def generate_sentences(content):
    # Break the generated script into sentences
    print("Generating sentences...")
    sentences = re.split(r'\n{2,}', content['script'])

    content['sentences'] = []

    for idx, sentence in enumerate(sentences):
      new_sentence = {
          'id': idx,
          'text': sentence,
          'keywords': [],
          'images': []
      }
      content['sentences'].append(new_sentence)
    
    print("Sentences generation complete.\n---")

  def generate_keywords(content):
    # Extract keywords from the generated sentences using OpenAI
    print("Generating keywords...")
    load_dotenv()

    openai.organization = os.environ.get('OPENAI_ORG_ID')
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    for idx, sentence in enumerate(content['sentences']):
      user_prompt = "Please identify the keywords in the following phrase:" + sentence['text'] + ". Do not include " + content['searchTerm'] + "Return only the keywords split by a comma."
      
      response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
      )
      
      sentence['keywords'] = response.choices[0].message.content.split(',')
      print(f"Keywords for sentence {idx} completed.")
    
    print("Keywords generation complete.\n---")

  # Execution of all functions
  fetch_news(content['searchTerm'])
  parse_news(content)
  generate_content(content)
  generate_script(content)
  generate_sentences(content)
  generate_keywords(content)

  # Save the modified content back using the handler
  handler.save(content)
