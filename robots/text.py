from pygooglenews import GoogleNews
import newspaper
import requests
import re

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

    print("News parsing comeplete.\n---")

  fetch_news(content['searchTerm'])
  parse_news(content)
  # generate_script(content)